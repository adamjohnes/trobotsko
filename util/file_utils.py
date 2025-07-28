import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
from logs.logging import load_logs_config
      
logging = load_logs_config()

async def store_file_procedure(fileName, fileUrl, savedPath):
  async with aiohttp.ClientSession() as session:
    async with session.get(fileUrl) as response:
      if response.status == 200: # success
        with open(savedPath, "wb") as file:
          file.write(await response.read())
        logging.info(f"Saved {fileName} to {savedPath}.")
      else:
        logging.info(f"Failed to save {fileName}.")