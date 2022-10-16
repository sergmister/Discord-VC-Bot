import requests
import discord
import tempfile
import nacl
import os

from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()

def tts(ctx, arg):
    url = 'https://api.uberduck.ai/speak-synchronous'

    payload = {
        "voice": "zwf",
        "pace": 1,
        "speech": arg
    }
    headers = {
        "accept": "application/json",
        "uberduck-id": "anonymous",
        "content-type": "application/json",
        "authorization": os.environ.get("UBERDUCK")
    }

    response = requests.post(url, json=payload, headers=headers)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio:
        audio.write(response.content)
        audio.flush()
        audio.seek(0)
        
        # if you get an error saying ffmpeg isnt defined or something along those lines you need to install ffmpeg (brew install ffmpeg)
        prepared_audio = discord.FFmpegPCMAudio(audio.name, executable='ffmpeg')
        ctx.guild.voice_client.play(prepared_audio, after=None)
        audio.close