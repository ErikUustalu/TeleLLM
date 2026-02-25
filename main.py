import asyncio
import os
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
LLM_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "qwen/qwen3-32b"
LLM_BASE_URL = "https://api.groq.com/openai/v1"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ai_client = AsyncOpenAI(
  api_key=LLM_API_KEY,
  base_url=LLM_BASE_URL
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = await ai_client.responses.create(
    model=MODEL,
    input=update.message.text
  )
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response.output_text)

if __name__ == "__main__":
  application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

  start_handler = CommandHandler("start", start)
  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
  application.add_handler(start_handler)
  application.add_handler(echo_handler)

  application.run_polling()