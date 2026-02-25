#TeleLLM - Customizable OpenAI-Compatible Telegram chatbot

A blazingly fast asynchronous Telegram chatbot powered by any openai compatible llm api (by default uses groqai)

## Features
* **Presistent memory** Saves the last 10 chat messages per user, allowing for continuous conversations
* **Built-in rate limiting** Allows setting a daily per user token limit
* **Asynchronous** Built with `python-telegram-bot` and `aiosqlite` for fast execution, allowing multiple simultaneous users
* **Blazingly fast** Groq api is incredably fast and has a free tier (Can be used with other openai-compatible apis too)

## Setup
1. **Clone this repository**
   `git clone https://github.com/ErikUustalu/TeleLLM.git`
2. **Install dependencies**
   `pip install -r requirements.txt`
3. **Configure enviorment variables**
   Rename .env.example to .env and add your api keys:
   ```
   TELEGRAM_API_KEY=your-telegram-api-key-here
   LLM_API_KEY=your-openai-compatible-api-key-here
   ```
4. **Run the bot**
   `python bot.py`
   The SQLite database bot.db will be automatically created