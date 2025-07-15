import asyncio
import discord
from classes.SongQueue import SongQueue

class BotAPI:
  def __init__(self):
    self.songList=SongQueue()
    self.currentChannel = None
    self.isConnected = False
    self.isRepeating = False
    self.VoiceClient = None 
   
  def __str__(self):
    return f"Details:\nCurrent Channel: {self.currentChannel}\nQueue:\n{self.songList}\nis Connected?: {self.isConnected}\nis Playing?: {self.VoiceClient.is_playing()}\nVoiceClient: {self.VoiceClient}"
  
  def setChannel(self, channel:str):
    self.channel = channel
    
  def setIsConnected(self, isConnected:bool):
    self.isConnected = isConnected
  
  def setVoiceClient(self, voiceClient:discord.VoiceClient):
    self.VoiceClient = voiceClient
  
  def setBotAttributes(self, channel:str, isConnected:bool, isRepeating:bool, VoiceClient:discord.VoiceClient):
    self.currentChannel = channel
    self.isConnected = isConnected
    self.isRepeating = isRepeating
    self.VoiceClient = VoiceClient
    
  # async def getSongs(self):
  #   stringBuilder : str = ''
  #   for song in self.songList:
  #     stringBuilder+=f"{song}\n"
  #   return stringBuilder