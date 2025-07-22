import asyncio
from classes.Song import Song
from classes.SongQueue import SongQueue

class Playlist:
  def __init__(self):
    self.userid = None
    self.name = None
    self.user = None
    self.playlist = SongQueue()
  
  def __str__(self):
    if (len(self.playlist) > 0):
      return f"Song Playlist: {self.name}\n".join("[" + str(self.playlist.index(song)) + "]  " + str(song) + '\n' for song in self.playlist)
    else:
      return f"No songs in playlist."
  
  def __repr__(self):
    return self.__str__()