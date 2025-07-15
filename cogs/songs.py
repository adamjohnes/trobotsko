import discord
from discord.ext import commands
from util.song_utils import determineMessageType
from cogs.moving import connectVoice

songs = ["https://www.youtube.com/watch?v=xKCek6_dB0M", "https://www.youtube.com/watch?v=a81eP2E8MEQ", "https://www.youtube.com/watch?v=_ILsdcs__ME", "Right above it", "the duck song", "Ariana Grande positions"]

class Song(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="play", help="submits a song to the queue, also plays song if none is playing -> Format: <play [Youtube URL] or <song [song title] --i.e. <song youtube.com/example")
  async def submitSong(self, ctx, *, songElement: str):
    # if (self.bot.Trobotsko.VoiceClient == None):
    #   await ctx.send("I need to join a voice channel first, use <join-voice")
    #   return
    if (self.bot.Trobotsko.isConnected == False):
      await connectVoice(self.bot, ctx)
    submittedSong = await determineMessageType(songElement)
    try:
      self.bot.Trobotsko.songList.pushSong(submittedSong)
      await ctx.send(f"Song added: {submittedSong}")
      if (self.bot.Trobotsko.VoiceClient.is_playing() == False):
        await self.bot.Trobotsko.songList.playSongs(self.bot, ctx)
    except Exception as e:
      await ctx.send(f"Error adding song to queue: {e}")
      
  @commands.command(name="test", help="creates test song list")
  async def inputSongs(self, ctx):
    for song in songs:
      try:
        self.bot.Trobotsko.songList.pushSong(await determineMessageType(song))
        await ctx.send(f"Song added: {song}")
      except Exception as e:
        await ctx.send(f"Error adding song to queue: {e}")
    
  @commands.command(name="pause", help="pauses currently playing song")
  async def pauseSong(self, ctx):
    await self.bot.Trobotsko.songList.pauseSong(self.bot, ctx)  
      
  @commands.command(name="resume", help="resumes current song")
  async def resumeSong(self, ctx):
    await self.bot.Trobotsko.songList.resumeSong(self.bot, ctx)  
      
  @commands.command(name="skip", help="skips the current song and removes it from the queue")
  async def skipSong(self, ctx):
    if (self.bot.Trobotsko.VoiceClient == None):
      return
    if (self.bot.Trobotsko.VoiceClient.is_paused()):
      await self.bot.Trobotsko.songList.resumeSong(self.bot, ctx)
    if (self.bot.Trobotsko.isRepeating):
      self.bot.Trobotsko.isRepeating = False
    self.bot.Trobotsko.VoiceClient.stop()
    self.bot.Trobotsko.songList.current = None
    await ctx.send(f"New Queue: \n{self.bot.Trobotsko.songList}")
  
  @commands.command(name="see", help="see a list of the songs in the queue")
  async def userSeeSongs(self, ctx):
    await ctx.send(f"\n{self.bot.Trobotsko.songList}")
      
  @commands.command(name="remove", help="remove a song in the queue\nFormat: <remove [Youtube URL] OR <remove [song title] OR <remove [position]")
  async def removeSong(self, ctx, songElement):
    try:
      self.bot.Trobotsko.songList.removeSong(ctx, songElement)
    except Exception as e:
      print(e)

  @commands.command(name="clear", help="clears the queue completely")
  async def clearQueue(self, ctx):
    self.bot.Trobotsko.songList.deleteQueue()

  @commands.command(name="reorder", help="randomizes the order of the songs in the queue")
  async def randomizeSongs(self, ctx):
    if (self.bot.Trobotsko.songList.getSize() > 0):
      await ctx.send(self.bot.Trobotsko.songList.randomizeOrder())

  @commands.command(name="repeat", help="toggles the song on/off repeat")
  async def repeatSong(self, ctx):
    await self.bot.Trobotsko.songList.repeatSong(self.bot, ctx)
    await ctx.send(f"Repeating... {self.bot.Trobotsko.songList.current}")

async def setup(bot):
  await bot.add_cog(Song(bot))