import asyncio
from classes.Song import Song

class Playlist:
  def __init__(self, userid=None, name=None):
    self.userid = userid
    self.name = name
    self.songList = []
  
  def __str__(self):
    return f"Title: {self.title}\nURL: {self.url}"
  
  def __repr__(self):
    return self.__str__()
  
  # add song
  
  # remove song
  
  