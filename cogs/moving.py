import discord
from discord.ext import commands
import asyncio

class MovingCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="join-voice", help="Joins the voice channel")
  async def join_voice(self, ctx):   
    if not ctx.author.voice: # User is not connected to a voice channel
      await ctx.send(f"{ctx.author} is not connected to a voice channel.")
      return

    channel = ctx.author.voice.channel # We only reach here if a user is connected to a voice channel

    if channel is self.bot.Trobotsko.currentChannel: # User and bot reside in same channel
      await ctx.send(f"{self.bot.user} already appears in exist inside of: {channel}")
      return
    elif channel is not self.bot.Trobotsko.currentChannel and self.bot.Trobotsko.currentChannel is not None: # User and bot reside in different channels
      await ctx.send(f"Joining... {channel}")
      try:
        await ctx.voice_client.disconnect()
        self.bot.Trobotsko.setBotAttributes(channel, False, None)
      except:
        await ctx.send("There was an issue attempting to leave the channel...")
        
    try: 
      self.bot.Trobotsko.setBotAttributes(channel, True, await channel.connect(reconnect=False))
    except discord.GatewayNotFound as e:
      await ctx.send(f"GatewayNotFound: {e}")
    except discord.ConnectionClosed as e:
      await ctx.send(f"ConnectionClosed: {e}")
    except discord.ClientException as e:
      await ctx.send(f"ClientException: {e}")
            
    if (self.bot.Trobotsko.VoiceClient is None):
      self.bot.Trobotsko.setBotAttributes(None, False, None)
            
  @commands.command(name = "leave-voice", help = "Leaves the voice channel")
  async def leave_voice(self, ctx):
    if not self.bot.Trobotsko.isConnected: # User is not connected to voice
      await ctx.send(f"{self.bot.user} is not connected to a voice channel.") 
    elif ctx.voice_client is not None: 
      try:
        self.bot.Trobotsko.setBotAttributes(None, False, await ctx.voice_client.disconnect())
      except:
        await ctx.send("There was an issue attempting to leave the channel...")

  @commands.command(name = "print", help = "print bot attributes")
  async def print(self, ctx):
    await ctx.send(self.bot.Trobotsko)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    if member.id == self.bot.user.id:
      self.bot.Trobotsko.currentChannel = after.channel # any movement between channels, we update the bots current channel
      

async def setup(bot):
  await bot.add_cog(MovingCog(bot))
