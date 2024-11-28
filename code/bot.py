import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client
from pytgcalls import PyTgCalls, idle
from tg_interface import setup_handlers

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("SLONbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

setup_handlers(app, call_py)


async def main():
    await app.start()
    await call_py.start()
    print("Бот запущен")
    await idle()


asyncio.run(main())
