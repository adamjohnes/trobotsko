from util.error_utils import LengthEqualsZeroError
import random
import asyncio
import discord

class SongQueue:
  def __init__(self):
    self.queue = []
    self.current = None
    self.previous = None
    self.isPlayingLoopActive = False
  
  def __str__(self):
    if (len(self.queue) != 0):
      return "".join("[" + str(self.queue.index(song)) + "]  " + str(song) + '\n' for song in self.queue)
    else:
      return "There are no songs in the queue."
  
  def get_size(self):
    return len(self.queue)
  
  def peek(self):
    if self.get_size() > 0:
      return self.queue[0]
    else:
      raise LengthEqualsZeroError("The length of the queue is 0.")
  
  def push_song(self, song):
    self.queue.append(song)
    
  def pop_song(self):
    self.queue.pop(0)
    
  async def remove_song(self, ctx, songElement):
    # pause song or stop playing if current playing song
    if (songElement.__contains__("https://www.youtube.com/") or songElement.__contains__("https://youtu.be/")): # dealing with an youtube URL
      await self.remove_by_URL(ctx, songElement)
    elif (songElement.isdigit()):
      if (int(songElement) >= 0): 
        await self.remove_by_position(ctx, songElement)
    else:
      await self.remove_by_title(ctx, songElement)
  
  async def remove_by_URL(self, ctx, url):
    for i, song in enumerate(self.queue):
      if song.url.lower().__contains__(url.lower()):
        try:
          await ctx.send(f"Removing... {self.queue[i]}")
          del self.queue[i]
        except Exception as e:
          print(e)
    
  async def remove_by_position(self, ctx, position):
    try:
      await ctx.send(f"Removing... {self.queue[int(position)]}")
      del self.queue[int(position)]
    except Exception as e:
      print(e)
      await ctx.send(f"A song with position: [{position}] doesn't exist.")
    
  async def remove_by_title(self, ctx, songTitle):
    for i, song in enumerate(self.queue):
      if song.title.lower().__contains__(songTitle.lower()):
        try:
          await ctx.send(f"Removing... {self.queue[i]}")
          del self.queue[i]
        except Exception as e:
          print(e)
          await ctx.send(f"A song with the title: [{songTitle}] doesn't exist.")

  def delete_queue(self):
    self.queue = []

  def randomize_order(self):
    random.shuffle(self.queue)
    return (f"```Order has been randomized... new queue:\n{self.queue}```")
  
  async def play_songs(self, bot, ctx):
    if (self.isPlayingLoopActive):
      return
    
    try:
      while True:
        if bot.Trobotsko.VoiceClient is None:         # disconnected
          break

        # If audio is repeating, don't act in here
        if bot.Trobotsko.isRepeating:
          await asyncio.sleep(0.5)
          continue

        # If audio is still playing or paused, just wait
        if bot.Trobotsko.VoiceClient.is_playing() or bot.Trobotsko.VoiceClient.is_paused():
          await asyncio.sleep(0.5)
          continue

        # Now it’s safe to quit if *nothing* is left
        if bot.Trobotsko.songList.get_size() == 0:
          break

        # Otherwise, start the next track…
        if bot.Trobotsko.isShuffling:
          randomNumber = random.randint(0, len(bot.Trobotsko.songList.queue) - 1)
          self.current = bot.Trobotsko.songList.queue[randomNumber]
          bot.Trobotsko.songList.queue.pop(randomNumber)
        else:
          self.current = bot.Trobotsko.songList.peek()
          bot.Trobotsko.songList.pop_song()
        await ctx.send(f"```Playing: {self.current}```")
        source = discord.FFmpegPCMAudio(self.current.playableAudio, options='-vn')
        bot.Trobotsko.VoiceClient.play(source)
        self.isPlayingLoopActive = True
    finally:
      self.isPlayingLoopActive = False 
      
  async def repeat_song(self, bot, ctx):
    bot.Trobotsko.isRepeating = not bot.Trobotsko.isRepeating
    if (bot.Trobotsko.isRepeating):
      await ctx.send(f"Repeating song... {bot.Trobotsko.songList.current}")
    else:
      await ctx.send(f"Repeat turned off.")
    while (bot.Trobotsko.isRepeating):
      if bot.Trobotsko.VoiceClient.is_playing() or bot.Trobotsko.VoiceClient.is_paused():
        await asyncio.sleep(0.5)
      else:
        try:
          source = discord.FFmpegPCMAudio(self.current.playableAudio, options='-vn')
          bot.Trobotsko.VoiceClient.play(source)
        except Exception as e:
          print(e)
      
  async def pause_song(self, bot, ctx):
    if (bot.Trobotsko.VoiceClient.is_paused() == False and bot.Trobotsko.VoiceClient.is_playing()):
      try:
        bot.Trobotsko.VoiceClient.pause()
        await ctx.send(f"Pausing...")
        return
      except Exception as e:
        print(e)
        await ctx.send(f"Bot has no song to pause.")
    else:
      await ctx.send(f"Bot has no song to pause.")
        
  async def resume_song(self, bot, ctx):
    if (bot.Trobotsko.VoiceClient.is_paused()):
      try:
        bot.Trobotsko.VoiceClient.resume()
        await ctx.send(f"Resuming...")
        return
      except Exception as e:
        print(e)
        await ctx.send(f"Bot has no song to resume.")
    else:
      await ctx.send(f"No song is paused.") 
      
  async def shuffle_songs(self, bot, ctx):
    bot.Trobotsko.isShuffling = not bot.Trobotsko.isShuffling
    if (bot.Trobotsko.isShuffling):
      await ctx.send(f"Shuffling queue...")
    else:
      await ctx.send(f"Turning off shuffling...")