import asyncio
from classes.Song import Song

class Playlist:
  def __init__(self):
    self.userid = None
    self.name = None
    self.user = None
    self.playlist = []
  
  def __str__(self):
    if (len(self.playlist) > 0):
      return f"Song Playlist: {self.name}\n".join("[" + str(self.playlist.index(song)) + "]  " + str(song) + '\n' for song in self.playlist)
    else:
      return f"No songs in playlist."
  
  def __repr__(self):
    return self.__str__()
  
  #create playlist
  async def create_playlist(self, ctx, name):
    self.userid = ctx.author.id
    self.name = name
    self.user = ctx.author.name
    
  # add song
  async def add_song(self, song):
    await self.playlist.append(song)
  
  # remove song
  async def remove_song(self, ctx, songElement):
    if (songElement.isdigit()):
      await self.remove_song_by_position(ctx, songElement)
    else:
      await self.remove_song_by_title(ctx, songElement)
      
  async def remove_song_by_position(self, ctx, position):
    try:
      del self.playlist[position]
    except Exception as e:
      print(e)
      await ctx.send(f"A song with position: [{position}] doesn't exist in {self.name}.")
  
  async def remove_song_by_title(self, ctx, songTitle):
    for i, song in enumerate(self.playlist):
      if song.title.lower().__contains__(songTitle.lower()):
        try:
          await ctx.send(f"Removing... {self.playlist[i]} from {self.name}.")
          del self.playlist[i]
        except Exception as e:
          print(e)
          await ctx.send(f"A song with the title: [{songTitle}] doesn't exist.")
      
  