import discord
from discord.ext import commands
import asyncio
import os
from util.file_utils import store_file_procedure
from util.db import insert_file_db, see_file_db, delete_file_db
from logs.logging import load_logs_config
from dotenv import load_dotenv

load_dotenv()
logging = load_logs_config()

class Files(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
            
  @commands.command(name = "store-file", help = "stores file for later retrieval")
  async def store_files(self, ctx, *, userAccessName=None):
    if not userAccessName:
      await ctx.send(f"❌ Please provide a name for your file (i.e. <store-file examplefilename)")
      return
    
    if not ctx.message.attachments:
      await ctx.send(f"❌ Please provide a file")
    
    if (await is_duplicate_access_name(self.bot, ctx, userAccessName)):
      await ctx.send(f"A file with access name: {userAccessName} already exists. Name it something else.")
    
    directory = f".\\user_storage\\{ctx.message.author.id}\\"
    os.makedirs(directory, exist_ok=True)
      
    for file in ctx.message.attachments:
      fileElements = await set_attributes(file, directory, userAccessName)
      print(fileElements)
      await store_file_procedure(fileElements['fileName'], fileElements['fileUrl'], fileElements['savedPath'])
      await insert_files_todb(self.bot, ctx, fileElements)

  # to-do: see files [metadata] (per user basis), send files  
  @commands.command(name = "see-files", help = "displays information about all the files a particular user has stored")
  async def see_files(self, ctx):
    directory = f".\\user_storage\\{ctx.message.author.id}\\"
    if not os.path.isdir(directory):
      await ctx.send("The user has no files stored.")
      return
    
    userFiles = await see_files_fromdb(self.bot, ctx)
    await ctx.send(f"__**Stored files for {ctx.author.name}**__")
    strBuilder = ''
    for fileInfo in userFiles:
      strBuilder+=f"File name: {fileInfo['filename']} --- Access Name: {fileInfo['accessname']} --- Created at: {fileInfo['created_at']}\n"
    await ctx.send(f"```{strBuilder}```")
  
  @commands.command(name = "get-file", help = "specifically returns a file's contents")
  async def get_file(self, ctx, *, userAccessName):
    directory = f".\\user_storage\\{ctx.message.author.id}\\"
    if not os.path.isdir(directory):
      await ctx.send("The user has no files stored.")
      return
    
    userFiles = await see_files_fromdb(self.bot, ctx)
    for fileInfo in userFiles:
      if (userAccessName == fileInfo["accessname"]):
        await ctx.send(file=discord.File(fileInfo["localpath"]))
        return
    
    await ctx.send(f"There was no file with access name: {userAccessName} found.")
    
  @commands.command(name = "delete-file", help = "delete a file and its contents")
  async def delete_file(self, ctx, *, userAccessName):
    directory = f".\\user_storage\\{ctx.message.author.id}\\"
    if not os.path.isdir(directory):
      await ctx.send("The user has no files stored.")
      return
    
    userFiles = await see_files_fromdb(self.bot, ctx)
    for fileInfo in userFiles:
      if (userAccessName == fileInfo["accessname"]):
        try:    
          os.remove(fileInfo["localpath"])
          await remove_file_fromdb(self.bot, ctx, userAccessName)
          await ctx.send(f"{userAccessName} was removed from memory.")
          return
        except Exception as e:
          logging.info(e)
    
    await ctx.send(f"There was no file with access name: {userAccessName} found.")
    
async def set_attributes(file, directory, userAccessName):
  fileStructure = {
    "fileName": None,
    "fileUrl": None,
    "savedPath": None,
    "accessName": None
  }
  
  if (file.filename == 'image.png' or file.filename == 'message.txt'):
    _, ext = os.path.splitext(file.filename)
    fileStructure.update({
      "fileName": f"{userAccessName}{ext}",
      "fileUrl": file.url,
      "savedPath": os.path.join(f"{directory}{userAccessName}{ext}"),
      "accessName": userAccessName
    })
  else:
    fileStructure.update({
      "fileName": file.filename,
      "fileUrl": file.url,
      "savedPath": os.path.join(directory, file.filename),
      "accessName": userAccessName
    })
    
  return fileStructure
  
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

async def see_files_fromdb(bot, ctx):
  loop = ctx.bot.loop  
  try:
    userFiles = await loop.run_in_executor(
      None,
      see_file_db, 
      bot.db_pool,
      ctx.author
    )
  except Exception as e:
    logging.info(e)
  return userFiles

async def remove_file_fromdb(bot, ctx, accessName):
  loop = ctx.bot.loop  
  try:
    userFiles = await loop.run_in_executor(
      None,
      delete_file_db, 
      bot.db_pool,
      ctx.author,
      accessName
    )
  except Exception as e:
    logging.info(e)

async def is_duplicate_access_name(bot, ctx, userAccessName):
  userFiles = await see_files_fromdb(bot, ctx)
  
  for fileInfo in userFiles:
    if (fileInfo['accessname'] == userAccessName):
      return True
    
  return False # we only ever get here if no duplicates are found

async def setup(bot):
  await bot.add_cog(Files(bot))
