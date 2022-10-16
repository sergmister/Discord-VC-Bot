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

#starts recording, processes it when it's done        
@client.command()
async def record(ctx):
    ctx.voice_client.start_recording(discord.sinks.WaveSink(), callback, ctx)
    await ctx.send("listening...") 

async def callback(sink, ctx):
  for i in range(0,len(sink.get_all_audio())):
      b = sink.get_all_audio()[i] 
      
      #print(b.read()) this was just for debugging

      #b is the BytesIO object
      #doing this creates an unreadable wav file
      with open(f"{str(i)}.wav", 'xb') as file:
          file.write(b.read())


#stops recording
@client.command()
async def stop(ctx):
    ctx.voice_client.stop_recording()

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