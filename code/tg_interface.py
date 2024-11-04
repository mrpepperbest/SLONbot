from pyrogram import filters
from music_interface import get_youtube_audio_url

current_track = None

def handle_play(app, pytgcalls):
    @app.on_message(filters.command("play"))
    async def play(client, message):
        global current_track
        chat_id = message.chat.id
        if len(message.text.split()) < 2:
            await message.reply("Please, specify track name after the keyword '/play'.")
            return
        
        track_name = message.text.split(maxsplit=1)[1]
        audio_url, track_title = get_youtube_audio_url(track_name)
        
        if audio_url:
            await pytgcalls.join_group_call(
                chat_id,
                audio_url
            )
            current_track = track_title
            await message.reply(f"Now playing: {track_title}")
        else:
            await message.reply("Unable to find the track.")

def handle_stop(app, pytgcalls):
    @app.on_message(filters.command("stop"))
    async def stop(client, message):
        chat_id = message.chat.id
        await pytgcalls.leave_group_call(chat_id)
        await message.reply("Broadcasting stopped.")
