import asyncio
import discord
from classes.SongQueue import SongQueue

class BotAPI:
  def __init__(self):
    self.songList=SongQueue()
    self.currentChannel = None
    self.isConnected = False
    self.isRepeating = False
    self.isShuffling = False
    self.VoiceClient = None 
   
  def __str__(self):
    return f"Details:\nCurrent Channel: {self.currentChannel}\nQueue:\n{self.songList}\nis Connected?: {self.isConnected}\nis Playing?: {self.VoiceClient.is_playing()}\nVoiceClient: {self.VoiceClient}"
  
  def set_channel(self, channel:str):
    self.channel = channel
    
  def set_is_connected(self, isConnected:bool):
    self.isConnected = isConnected
  
  def set_voice_client(self, voiceClient:discord.VoiceClient):
    self.VoiceClient = voiceClient
  
  def set_bot_attributes(self, channel:str, isConnected:bool, isRepeating:bool, VoiceClient:discord.VoiceClient):
    self.currentChannel = channel
    self.isConnected = isConnected
    self.isRepeating = isRepeating
    self.VoiceClient = VoiceClient
    self.isShuffling = False