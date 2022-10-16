import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

from tts import *
#from parseStatement import *

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='&',intents=intents)

#join vc
@client.command()
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect()
  else:
    await ctx.send("not in a voice channel!")

#leave vc
@client.command()
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.voice_client.disconnect()
  else:
    await ctx.send("not in a voice channel!")

#play tts audio from command
@client.command()
async def play(ctx, *, arg):
  tts(ctx,arg)
        
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.author == client.user:
      return

  #ping
  if message.content.startswith('ping'):
      await message.channel.send('pong')

client.run(os.environ.get("DISCORD"))