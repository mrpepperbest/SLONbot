import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from music_interface import get_youtube_audio_url

current_track = None
idle_timer = None


async def check_idle(chat_id, call_py):
    await asyncio.sleep(600)
    if not current_track:
        await call_py.leave_call(chat_id)
        print("Bot left the call after 10 min AFK.")


def reset_idle_timer(chat_id, call_py):
    global idle_timer
    if idle_timer:
        idle_timer.cancel()
    idle_timer = asyncio.create_task(check_idle(chat_id, call_py))


def setup_handlers(app: Client, call_py: PyTgCalls):
    @app.on_message(filters.command("start"))
    async def start_handler(client, message: Message):
        await message.reply("Hello! The bot is running and ready to receive commands.")
    
    @app.on_message(filters.command("play"))
    async def play_handler(client, message: Message):
        global current_track
        chat_id = message.chat.id
        if len(message.text.split()) < 2:
            await message.reply("Please, specify the track name after the keyword '/play'.")
            return

        track_name = message.text.split(maxsplit=1)[1]
        audio_url, track_title = get_youtube_audio_url(track_name)

        if audio_url:
            await call_py.play(chat_id, MediaStream(audio_url))
            current_track = track_title
            await message.reply(f"Now playing: {track_title}")
            reset_idle_timer(chat_id, call_py)
        else:
            await message.reply("Unable to find the track.")

    @app.on_message(filters.command("pause"))
    async def pause_handler(client, message: Message):
        await call_py.pause_stream(message.chat.id)
        await message.reply("Playback paused.")
        reset_idle_timer(message.chat.id, call_py)

    @app.on_message(filters.command("resume"))
    async def resume_handler(client, message: Message):
        await call_py.resume_stream(message.chat.id)
        await message.reply("Playback resumed.")
        reset_idle_timer(message.chat.id, call_py)

    @app.on_message(filters.command("stop"))
    async def stop_handler(client, message: Message):
        global current_track
        await call_py.leave_call(message.chat.id)
        current_track = None
        await message.reply("Playback stopped and left the call.")
        reset_idle_timer(message.chat.id, call_py)

    @app.on_message(filters.command("leave"))
    async def leave_handler(client, message: Message):
        await call_py.leave_call(message.chat.id)
        await message.reply("Left the call.")
