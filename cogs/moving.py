import discord
from discord.ext import commands
import asyncio

class MovingCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="join-voice", help="Joins the voice channel")
  async def join_voice(self, ctx):   
    await connectVoice(self.bot, ctx)
            
  @commands.command(name = "leave-voice", help = "Leaves the voice channel")
  async def leave_voice(self, ctx):
    await disconnectVoice(self.bot, ctx)

  @commands.command(name = "print", help = "print bot attributes")
  async def print(self, ctx):
    await ctx.send(self.bot.Trobotsko)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    if member.id == self.bot.user.id:
      self.bot.Trobotsko.currentChannel = after.channel # any movement between channels, we update the bots current channel
      

async def connectVoice(bot, ctx):
  if not ctx.author.voice: # User is not connected to a voice channel
    await ctx.send(f"{ctx.author} is not connected to a voice channel.")
    return

  channel = ctx.author.voice.channel # We only reach here if a user is connected to a voice channel

  if channel is bot.Trobotsko.currentChannel: # User and bot reside in same channel
    await ctx.send(f"{bot.user} already appears in exist inside of: {channel}")
    return
  elif channel is not bot.Trobotsko.currentChannel and bot.Trobotsko.currentChannel is not None: # User and bot reside in different channels
    await ctx.send(f"Joining... {channel}")
    try:
      await ctx.voice_client.disconnect()
      bot.Trobotsko.setBotAttributes(channel, False, None)
    except:
      await ctx.send("There was an issue attempting to leave the channel...")
      
  try: 
    bot.Trobotsko.setBotAttributes(channel, True, await channel.connect(reconnect=False))
  except discord.GatewayNotFound as e:
    await ctx.send(f"GatewayNotFound: {e}")
  except discord.ConnectionClosed as e:
    await ctx.send(f"ConnectionClosed: {e}")
  except discord.ClientException as e:
    await ctx.send(f"ClientException: {e}")
          
  if (bot.Trobotsko.VoiceClient is None):
    bot.Trobotsko.setBotAttributes(None, False, None)
    
async def disconnectVoice(bot, ctx):
  if not bot.Trobotsko.isConnected: # User is not connected to voice
    await ctx.send(f"{bot.user} is not connected to a voice channel.") 
  elif ctx.voice_client is not None: 
    try:
      if (bot.Trobotsko.VoiceClient.is_playing()):
        bot.Trobotsko.VoiceClient.stop()
        
      await ctx.voice_client.disconnect()
      bot.Trobotsko.setBotAttributes(None, False, None)
    except:
      await ctx.send("There was an issue attempting to leave the channel...")

async def setup(bot):
  await bot.add_cog(MovingCog(bot))
