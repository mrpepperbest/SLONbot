import logging
import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from yt_dlp import YoutubeDL
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

logging.basicConfig(level=logging.INFO)

current_track = None

def get_youtube_audio_url(track_name):
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch:{track_name}", download=False)['entries'][0]
            return info_dict['url'], info_dict['title']
        except Exception as e:
            logging.error(f"Не удалось найти или загрузить аудио: {e}")
            return None, None

async def start_stream(chat_id, track_name):
    global current_track
    audio_url, track_title = get_youtube_audio_url(track_name)
    
    if audio_url:
        await pytgcalls.join_group_call(chat_id, audio_url)
        current_track = track_title
        return track_title
    else:
        return None

@pytgcalls.on_stream_end()
async def on_stream_end(update: Update):
    if isinstance(update, StreamAudioEnded):
        global current_track
        current_track = None
        print("Аудио завершилось")

@app.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    if len(message.text.split()) < 2:
        await message.reply("Пожалуйста, укажите название трека после команды /play.")
        return
    
    track_name = message.text.split(maxsplit=1)[1]
    track_title = await start_stream(chat_id, track_name)
    
    if track_title:
        await message.reply(f"Сейчас играет: {track_title}")
    else:
        await message.reply("Не удалось найти трек.")

@app.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply("Воспроизведение остановлено.")

app.start()
pytgcalls.run()
