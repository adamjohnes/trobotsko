import discord
from discord.ext import commands
import asyncio
import os
from util.file_utils import store_file_procedure

class Files(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
            
  @commands.command(name = "store-files", help = "stores file for later retrieval")
  async def store_files(self, ctx):
    directory = f".\\user_storage\\{ctx.message.author.id}\\"
    os.makedirs(directory, exist_ok=True)
    
    for file in ctx.message.attachments:
      fileName = file.filename
      fileUrl = file.url
      savedPath = os.path.join(directory, fileName)
      await store_file_procedure(fileName, fileUrl, savedPath)
      # [store file metadata in db]

  # to-do: store files [metadata], see files [metadata] (per user basis), send files  
  @commands.command(name = "command2")
  async def print(self, ctx, *, elements):
    await ctx.send(elements)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    pass
    
async def do_something(bot, ctx):
  pass

async def setup(bot):
  await bot.add_cog(Files(bot))
