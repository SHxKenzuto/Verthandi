import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext.commands.errors import MissingRequiredArgument
import streamlink
import re
bot = commands.Bot(command_prefix="$")

def audioGenerator(url_stream):
    ffmpeg_options = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn -hide_banner -loglevel error'}
    stream = streamlink.streams(url_stream)
    audio = stream["audio_only"]
    return FFmpegPCMAudio(audio.url,**ffmpeg_options)

@bot.command()
async def stream(ctx,msg):
    if ctx.message.author.voice==None:
        await ctx.send("You have to be in a voice channel in order to use this command")
        return
    elif re.fullmatch(r"https:\/\/www.twitch.tv\/.+",msg) == None:
        await ctx.send("You have to use a twitch channel link")
        return
    voice_channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels,name=voice_channel.name)
    voice_client=discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice_client == None or not voice_client.is_playing():
        if voice_client == None:
            voice_client = await voice.connect()
        elif voice_channel != voice_client:
            await voice_client.move_to(voice_channel)
        await ctx.send(msg)
        audio = audioGenerator(msg)
        voice_client.play(audio)

@bot.command()
async def skip(ctx):
	if ctx.message.author.voice==None:
		await ctx.send("You have to be in a voice channel in order to use this command")
		return
	voice_client=discord.utils.get(bot.voice_clients,guild=ctx.guild)
	if  voice_client!=None and voice_client.is_playing() and ctx.message.author.voice.channel == voice_client.channel:
		voice_client.stop()

@bot.command()
async def leave(ctx):
	if ctx.message.author.voice==None:
		await ctx.send("You have to be in a voice channel in order to use this command")
		return
	voice_client=discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if  voice_client!=None and ctx.message.author.voice.channel == voice_client.channel:
		await voice_client.disconnect()
   
@bot.event
async def on_ready():
	print("Verthandi Bot Started")

@bot.event
async def on_command_error(ctx,error):
	if isinstance(error,MissingRequiredArgument):
		await ctx.send("This command needs an argument")
  
bot.run("")

print("Verthandi Bot Stopped")

#274881137664
