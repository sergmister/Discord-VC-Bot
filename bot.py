import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

import whisper

from tts import tts
from parse_statement import parse

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="&", intents=intents)

# model = whisper.load_model("base")
model = whisper.load_model("small")

# join vc
@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("not in a voice channel!")


# leave vc
@client.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("not in a voice channel!")


# play tts audio from command
@client.command()
async def play(ctx, *, arg):
    tts(ctx, arg)


@client.command()
async def listen(ctx):
    if ctx.voice_client:
        ctx.voice_client.start_recording(discord.sinks.WaveSink(), callback, ctx)
        await ctx.send("listening...")
    else:
        await ctx.send("not in a voice channel!")


async def callback(sink: discord.sinks, ctx):
    for user_id, audio in sink.audio_data.items():
        if user_id == ctx.author.id:
            audio: discord.sinks.core.AudioData = audio
            print(user_id)
            filename = "audio.wav"
            with open(filename, "wb") as f:
                f.write(audio.file.getvalue())
            text = model.transcribe(filename)["text"]
            os.remove(filename)
            print(f"Received from {ctx.author.name}: {text}")
            reply = parse(text)
            print(f"Reply: {reply}")
            tts(ctx, reply)


# stops recording
@client.command()
async def stop(ctx):
    ctx.voice_client.stop_recording()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    # ping
    if message.content.startswith("ping"):
        await message.channel.send("pong")


client.run(os.environ.get("DISCORD"))
