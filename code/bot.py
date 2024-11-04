import os
from dotenv import load_dotenv
from pyrogram import Client
from pytgcalls import PyTgCalls
from tg_interface import setup_handlers

# Загрузка переменных окружения из .env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создание клиента Pyrogram и PyTgCalls
app = Client("SLONbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

# Настройка обработчиков команд
setup_handlers(app, call_py)

# Запуск PyTgCalls и Pyrogram
async def main():
    await app.start()
    await call_py.start()
    print("Бот запущен")
    await idle()  # Ожидание завершения

import asyncio
asyncio.run(main())
