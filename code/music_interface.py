import logging
from yt_dlp import YoutubeDL

def get_youtube_audio_url(track_name):
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch:{track_name}", download=False)['entries'][0]
            return info_dict['url'], info_dict['title']
        except Exception as e:
            logging.error(f"Не удалось найти или загрузить аудио: {e}")
            return None, None
