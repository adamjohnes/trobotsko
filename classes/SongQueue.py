from util.error_utils import LengthEqualsZeroError
import random

class SongQueue:
  def __init__(self):
    self.queue = []
    self.currentlyPlaying = None
  
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
    
  def removeSong(self, songElement):
    # pause song or stop playing if current playing song
    if (songElement.__contains__("https://www.youtube.com/") or songElement.__contains__("https://youtu.be/")): # dealing with an youtube URL
      self.removeByURL(songElement)
    elif (songElement.isdigit()):
      if (int(songElement) >= 0): 
        self.removeByPosition(songElement)
    else:
      self.removeByTitle(songElement)
  
  def removeByURL(self, url):
    for i, song in enumerate(self.queue):
      if song.url.lower() == url.lower():
        try:
          del self.queue[i]
        except Exception as e:
          print(e)
    
  def removeByPosition(self, position):
    for i, song in enumerate(self.queue):
      if (str(i) == str(position)):
        try:
          del self.queue[i]
        except Exception as e:
          print(e)
    
  def removeByTitle(self, songTitle):
    for i, song in enumerate(self.queue):
      if song.title.lower() == songTitle.lower():
        try:
          del self.queue[i]
        except Exception as e:
          print(e)

  def deleteQueue(self):
    self.queue = []

  def randomizeOrder(self):
    random.shuffle(self.queue)
    return (f"Order has been randomized... new queue:\n{self.queue}")