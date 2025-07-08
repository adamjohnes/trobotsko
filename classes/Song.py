import asyncio

class Song:
  def __init__(self, title=None, url=None):
    self.title = title
    self.url = url
  
  def __str__(self):
    return f"Title: {self.title}\nURL: {self.url}"
  
  def __repr__(self):
    return self.__str__()