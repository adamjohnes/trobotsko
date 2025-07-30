import discord
from discord.ext import commands
import asyncio
import os
from util.file_utils import store_file_procedure
from util.db import insert_file_db
from logs.logging import load_logs_config
from dotenv import load_dotenv

load_dotenv()
logging = load_logs_config()

class Files(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
            
  @commands.command(name = "store-file", help = "stores file for later retrieval")
  async def store_files(self, ctx, *, name):
    directory = f".\\user_storage\\{ctx.message.author.id}\\"
    os.makedirs(directory, exist_ok=True)
    
    if not name or name == '':
      name = ctx.message.attachment.filename
      
    for file in ctx.message.attachments:
      fileElements = await set_attributes(file, directory, name)
      await store_file_procedure(fileElements['fileName'], fileElements['fileUrl'], fileElements['savedPath'])
      await insert_files_todb(self.bot, ctx, fileElements)

  # to-do: see files [metadata] (per user basis), send files  
  @commands.command(name = "command2")
  async def print(self, ctx, *, elements):
    await ctx.send(elements)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    pass
    
async def set_attributes(file, directory, name):
  return {
    "fileName": file.filename,
    "fileUrl": file.url,
    "savedPath": os.path.join(directory, file.filename),
    "name": name
  }
  
async def insert_files_todb(bot, ctx, fileElements):
  loop = ctx.bot.loop  
  try:
    await loop.run_in_executor(
      None,
      insert_file_db, 
      bot.db_pool,
      ctx.author,
      fileElements
    )
  except Exception as e:
    logging.info(e)

async def setup(bot):
  await bot.add_cog(Files(bot))
