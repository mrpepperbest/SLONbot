import os
from dotenv import load_dotenv
from pyrogram import Client
from pytgcalls import PyTgCalls
from tg_interface import handle_play, handle_stop

load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

app = Client("SLONbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

handle_play(app, pytgcalls)
handle_stop(app, pytgcalls)

pytgcalls.start()
app.run()
