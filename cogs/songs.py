import discord
from discord.ext import commands
import asyncio
from classes.Song import Song
from util.song_utils import getURLFromTitle, fetchFromYoutubeURL


class SongCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="song", help="submit a song to the queue\nFormat: <song [Youtube URL] or <song [song title] --i.e. <song youtube.com/example")
  async def submitSong(self, ctx, *, songElement: str):
    submittedSong = None
    if (songElement.__contains__("https://www.youtube.com/") or songElement.__contains__("https://youtu.be/")): # dealing with an youtube URL
      submittedSong = await fetchFromYoutubeURL(songElement)
    else:
      submittedSong = await getURLFromTitle(songElement)
    try:
      self.bot.Trobotsko.songList.pushSong(submittedSong)
      await ctx.send(f"Song added: {submittedSong}")
    except Exception as e:
      await ctx.send(f"Error adding song to queue: {e}")
      
  @commands.command(name="skip", help="skips the current song and removes it from the queue")
  async def skipSong(self, ctx):
    self.bot.Trobotsko.songList.popSong()
    await ctx.send(f"New Queue: \n{self.bot.Trobotsko.songList}")
  
  @commands.command(name="see-songs", help="see a list of the songs in the queue")
  async def userSeeSongs(self, ctx):
    await ctx.send(self.bot.Trobotsko.songList)
    self.bot.Trobotsko.songList.peek()
      
  ## To-do: Implement remove song based off the input, whether it be URL, position, or title
  @commands.command(name="remove", help="remove a song in the queue\nFormat: <remove [Youtube URL] OR <remove [song title] OR <remove [position]")
  async def removeSong(self, ctx, songElement):
    try:
      self.bot.Trobotsko.songList.removeSong(songElement)
    except Exception as e:
      print(e)
      
    
async def setup(bot):
  await bot.add_cog(SongCog(bot))