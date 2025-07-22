import discord
from discord.ext import commands
from util.song_utils import determine_message_type
from cogs.moving import connect_voice

songs = ["https://www.youtube.com/watch?v=xKCek6_dB0M", "https://www.youtube.com/watch?v=a81eP2E8MEQ", "https://www.youtube.com/watch?v=_ILsdcs__ME", "Right above it", "the duck song", "Ariana Grande positions"]

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="add", help="submits a song to the queue, also plays song if none is playing")
  async def submit_song(self, ctx, *, songElement: str):
    # if (self.bot.Trobotsko.VoiceClient == None):
    #   await ctx.send("I need to join a voice channel first, use <join-voice")
    #   return
    if (self.bot.Trobotsko.isConnected == False):
      connectionStatus = await connect_voice(self.bot, ctx)
      if (connectionStatus == -1): # The caller is not connected to voice
        return
    submittedSong = await determine_message_type(songElement)
    try:
      self.bot.Trobotsko.songList.push_song(submittedSong)
      await ctx.send(f"```Song added: {submittedSong}```")
      if (self.bot.Trobotsko.VoiceClient.is_playing() == False):
        await self.bot.Trobotsko.songList.play_songs(self.bot, ctx)
    except Exception as e:
      await ctx.send(f"Error adding song to queue.")
      print(e)
  
  @commands.command(name="play", help="plays song from queue if none is playing")
  async def play_song(self, ctx):
    if (self.bot.Trobotsko.VoiceClient == None):
      await ctx.send("I need to join a voice channel first, use <join-voice")
      return
    if not ctx.author.voice: # User is not connected to a voice channel
      await ctx.send(f"{ctx.author} is not connected to a voice channel.")
    if (self.bot.Trobotsko.VoiceClient.is_playing() == False):
      await self.bot.Trobotsko.songList.play_songs(self.bot, ctx)
  
  @commands.command(name="test", help="creates test song list")
  async def input_songs(self, ctx):
    for song in songs:
      try:
        self.bot.Trobotsko.songList.push_song(await determine_message_type(song))
        await ctx.send(f"Song added: {song}")
      except Exception as e:
        await ctx.send(f"Error adding song to queue.")
        print(e)
    
  @commands.command(name="pause", help="pauses currently playing song")
  async def pause_song(self, ctx):
    await self.bot.Trobotsko.songList.pause_song(self.bot, ctx)  
      
  @commands.command(name="resume", help="resumes current song")
  async def resume_song(self, ctx):
    await self.bot.Trobotsko.songList.resume_song(self.bot, ctx)  
      
  @commands.command(name="skip", help="skips the current song and removes it from the queue")
  async def skip_song(self, ctx):
    if (self.bot.Trobotsko.VoiceClient == None):
      return
    if (self.bot.Trobotsko.VoiceClient.is_paused()):
      await self.bot.Trobotsko.songList.resume_song(self.bot, ctx)
    if (self.bot.Trobotsko.isRepeating):
      self.bot.Trobotsko.isRepeating = False
    self.bot.Trobotsko.VoiceClient.stop()
    self.bot.Trobotsko.songList.current = None
  
  @commands.command(name="see", help="see a list of the songs in the queue")
  async def see_songs(self, ctx):
    await ctx.send(f"\n```{self.bot.Trobotsko.songList}```")
      
  @commands.command(name="remove", help="remove a song in the queue")
  async def remove_song(self, ctx, songElement):
    try:
      await self.bot.Trobotsko.songList.remove_song(ctx, songElement)
    except Exception as e:
      print(e)

  @commands.command(name="clear", help="clears the queue completely")
  async def clear_queue(self, ctx):
    self.bot.Trobotsko.songList.delete_queue()

  @commands.command(name="reorder", help="one-time randomizes the order of the songs in the queue")
  async def randomize_songs(self, ctx):
    if (self.bot.Trobotsko.songList.get_size() > 0):
      await ctx.send(self.bot.Trobotsko.songList.randomize_order())

  @commands.command(name="repeat", help="toggles the song on/off repeat")
  async def repeat_song(self, ctx):
    await self.bot.Trobotsko.songList.repeat_song(self.bot, ctx)
    
  @commands.command(name="shuffle", help="puts the queue on shuffle mode")
  async def shuffle_songs(self, ctx):
    await self.bot.Trobotsko.songList.shuffle_songs(self.bot, ctx)

async def setup(bot):
  await bot.add_cog(Music(bot))