#TeleLLM - Customizable OpenAI-Compatible Telegram chatbot

A blazingly fast asynchronous Telegram chatbot powered by any openai compatible llm api (by default uses groqai)

[**Try it yourself**](https://t.me/erikuustalu_telellm_bot)
## Features

- **Presistent memory** Saves the last 10 chat messages per user, allowing for continuous conversations
- **Built-in rate limiting** Allows setting a daily per user token limit
- **Asynchronous** Built with `python-telegram-bot` and `aiosqlite` for fast execution, allowing multiple simultaneous users
- **Blazingly fast** Groq api is incredably fast and has a free tier (Can be used with other openai-compatible apis too)

## Setup

## CLI

**Prerequisities:** Python (3.14 tested)

1. **Clone this repository**
   `git clone https://github.com/ErikUustalu/TeleLLM.git`
2. **Install dependencies**
   `pip install -r requirements.txt`
3. **Configure enviorment variables**
   Rename .env.example to .env and add your api keys
4. **Run the bot**
   `python bot.py`
   The SQLite database bot.db will be automatically created

## Docker compose

**Prerequisities:** Docker

1.  **Create the .env file**
    * `nano .env`
    * Paste in the contents of [.env.example](https://github.com/ErikUustalu/TeleLLM/blob/main/.env.example) and modify them with your information
2.  **Create the database file**
    * `touch bot.db`
3.  **Create the docker compose file**
    * `nano docker-compose.yml`
    * Paste in the [docker-compose.yaml](https://github.com/ErikUustalu/TeleLLM/blob/main/docker-compose.yaml)
4.  **Start the bot**
    * `docker compose up -d`