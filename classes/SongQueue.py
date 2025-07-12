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
  
  def getSize(self):
    return len(self.queue)
  
  def peek(self):
    if self.getSize() > 0:
      return self.queue[0]
    else:
      raise LengthEqualsZeroError("The length of the queue is 0.")
  
  def pushSong(self, song):
    self.queue.append(song)
    
  def popSong(self):
    self.queue.pop(0)
    
  def removeSong(self, ctx, songElement):
    # pause song or stop playing if current playing song
    if (songElement.__contains__("https://www.youtube.com/") or songElement.__contains__("https://youtu.be/")): # dealing with an youtube URL
      self.removeByURL(ctx, songElement)
    elif (songElement.isdigit()):
      if (int(songElement) >= 0): 
        self.removeByPosition(ctx, songElement)
    else:
      self.removeByTitle(ctx, songElement)
  
  async def removeByURL(self, ctx, url):
    for i, song in enumerate(self.queue):
      if song.url.lower() == url.lower():
        try:
          del self.queue[i]
          await ctx.send(f"Removing... {self.queue[i]}")
        except Exception as e:
          print(e)
    
  async def removeByPosition(self, ctx, position):
    for i, song in enumerate(self.queue):
      if (str(i) == str(position)):
        try:
          del self.queue[i]
          await ctx.send(f"Removing... {self.queue[i]}")
        except Exception as e:
          print(e)
    
  async def removeByTitle(self, ctx, songTitle):
    for i, song in enumerate(self.queue):
      if song.title.lower() == songTitle.lower():
        try:
          del self.queue[i]
          await ctx.send(f"Removing... {self.queue[i]}")
        except Exception as e:
          print(e)

  def deleteQueue(self):
    self.queue = []

  def randomizeOrder(self):
    random.shuffle(self.queue)
    return (f"Order has been randomized... new queue:\n{self.queue}")
  
  async def playSongs(self, bot, ctx):
    if (self.isPlayingLoopActive):
      return
    
    try:
      while True:
        vc = bot.Trobotsko.VoiceClient
        if vc is None:         # disconnected
            break

        # If audio is still playing or paused, just wait
        if vc.is_playing() or vc.is_paused():
            await asyncio.sleep(0.5)
            continue

        # Now it’s safe to quit if *nothing* is left
        if bot.Trobotsko.songList.getSize() == 0:
            break

        # Otherwise, start the next track…
        self.current = bot.Trobotsko.songList.peek()
        bot.Trobotsko.songList.popSong()
        await ctx.send(f"Playing: {self.current}")
        source = discord.FFmpegPCMAudio(self.current.playableAudio, options='-vn')
        vc.play(source)
    finally:
      self.isPlayingLoopActive = False 
      
  async def pauseSong(self, bot, ctx):
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
        
  async def resumeSong(self, bot, ctx):
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