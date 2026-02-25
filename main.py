import asyncio
import os
import logging
import aiosqlite
import datetime
from openai import AsyncOpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
LLM_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "qwen/qwen3-32b"
LLM_BASE_URL = "https://api.groq.com/openai/v1"
DB_FILE = "bot.db"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ai_client = AsyncOpenAI(
  api_key=LLM_API_KEY,
  base_url=LLM_BASE_URL
)

async def init_db():
  async with aiosqlite.connect(DB_FILE) as db:
    await db.execute("CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY, tokens_today INTEGER DEFAULT 0, last_active TEXT)")
    await db.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, role TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(uid) REFERENCES users(uid))")
    await db.commit()

async def user(uid):
  async with aiosqlite.connect(DB_FILE) as db:
    async with db.execute("SELECT tokens_today, last_active FROM users WHERE uid = ?", (uid,)) as cursor:
      user = await cursor.fetchone()

    if not user:
      await db.execute("INSERT INTO users (uid, last_active) VALUES (?, ?)", (uid,datetime.date.today().isoformat(),))
      await db.commit()
      return True
    elif user[1] != datetime.date.today().isoformat():
      await db.execute("UPDATE users SET tokens_today = 0, last_active = ? WHERE uid = ?", (datetime.date.today().isoformat(), uid,))
      await db.commit()
      return True
    elif user[0] < 50000:
      return True
    elif user[0] >= 50000:
      return False
    
async def get_history_messages(uid):
  async with aiosqlite.connect(DB_FILE) as db:
    async with db.execute("SELECT role, message FROM messages WHERE uid = ? ORDER BY id DESC LIMIT 10", (uid,)) as cursor:
      history = await cursor.fetchall()

    history.reverse()
    messages = []
    for chat in history:
      if chat[0] == "user":
        messages.append({"role": "user", "content": chat[1]})
      else:
        messages.append({"role": "assistant", "content": chat[1]})

    return messages
    
async def add_to_history(uid, role, message):
  async with aiosqlite.connect(DB_FILE) as db:
    await db.execute("INSERT INTO messages (uid, role, message) VALUES (?, ?, ?)", (uid, role, message))
    await db.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if await user(update.effective_user.id):
    await add_to_history(update.effective_user.id, "user", update.message.text)
    messages = await get_history_messages(update.effective_user.id)
    response = await ai_client.chat.completions.create(
      model=MODEL,
      messages=messages
    )
    
    reply = response.choices[0].message.content

    for i in range(0, len(reply), 4095):
      chunk = reply[i:i+4095]
      await context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)

    await add_to_history(update.effective_user.id, "assistant", reply)

if __name__ == "__main__":
  asyncio.run(init_db())

  application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

  start_handler = CommandHandler("start", start)
  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
  application.add_handler(start_handler)
  application.add_handler(echo_handler)

  application.run_polling()