import discord
from discord.ext import commands
import asyncio
from classes.Song import Song
from util.song_utils import determineMessageType
from discord import FFmpegPCMAudio

songs = ["https://www.youtube.com/watch?v=xKCek6_dB0M", "https://www.youtube.com/watch?v=a81eP2E8MEQ", "https://www.youtube.com/watch?v=_ILsdcs__ME", "Right above it", "the duck song", "Ariana Grande positions"]

# to-do: clean up song logic
# test url: https://www.youtube.com/watch?v=jHjFxJVeCQs

class SongCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="song", help="submit a song to the queue\nFormat: <song [Youtube URL] or <song [song title] --i.e. <song youtube.com/example")
  async def submitSong(self, ctx, *, songElement: str):
    if self.bot.Trobotsko.VoiceClient == None:
      await ctx.send("I need to join a voice channel first, use <join-voice")
      return
    submittedSong = await determineMessageType(songElement)
    try:
      self.bot.Trobotsko.songList.pushSong(submittedSong)
      await ctx.send(f"Song added: {submittedSong}")
    except Exception as e:
      await ctx.send(f"Error adding song to queue: {e}")
    if (self.bot.Trobotsko.VoiceClient.is_playing() == False):
      try:
        print(f"Playing audio URL: {submittedSong}")
        source = discord.FFmpegPCMAudio(submittedSong.playableAudio, options='-vn')
        self.bot.Trobotsko.VoiceClient.play(source)
        await nextSong(self.bot.Trobotsko)
      except Exception as e:
        print(f"FFmpeg error: {e}")
      
  @commands.command(name="test", help="creates test song list")
  async def inputSongs(self, ctx):
    for song in songs:
      try:
        self.bot.Trobotsko.songList.pushSong(await determineMessageType(song))
        await ctx.send(f"Song added: {song}")
      except Exception as e:
        await ctx.send(f"Error adding song to queue: {e}")
    
      
  @commands.command(name="skip", help="skips the current song and removes it from the queue")
  async def skipSong(self, ctx):
    if (self.bot.Trobotsko.VoiceClient == None):
      return
    self.bot.Trobotsko.VoiceClient.stop()
    self.bot.Trobotsko.songList.popSong()
    await ctx.send(f"New Queue: \n{self.bot.Trobotsko.songList}")
  
  @commands.command(name="see", help="see a list of the songs in the queue")
  async def userSeeSongs(self, ctx):
    await ctx.send(f"\n{self.bot.Trobotsko.songList}")
      
  @commands.command(name="remove", help="remove a song in the queue\nFormat: <remove [Youtube URL] OR <remove [song title] OR <remove [position]")
  async def removeSong(self, ctx, songElement):
    try:
      self.bot.Trobotsko.songList.removeSong(songElement)
    except Exception as e:
      print(e)

  @commands.command(name="clear", help="clears the queue completely")
  async def clearQueue(self, ctx):
    self.bot.Trobotsko.songList.deleteQueue()

  @commands.command(name="reorder", help="randomizes the order of the songs in the queue")
  async def randomizeSongs(self, ctx):
    if (self.bot.Trobotsko.songList.getSize() > 0):
      await ctx.send(self.bot.Trobotsko.songList.randomizeOrder())

async def nextSong(bot):
  while True:
    while (bot.VoiceClient.is_playing() and bot.songList.getSize() > 0):
      await asyncio.sleep(10)
    bot.songList.popSong()
    source = discord.FFmpegPCMAudio(bot.songList.peek().playableAudio, options='-vn')
    bot.VoiceClient.play(source)

async def setup(bot):
  await bot.add_cog(SongCog(bot))