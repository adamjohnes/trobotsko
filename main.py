import discord
from discord.ext import commands
import asyncio
from classes.BotAPI import BotAPI
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='<', intents=intents)
bot.Trobotsko = BotAPI()

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
  await ctx.send("Shutting down.")
  await bot.close()

async def setup():
  for ext in ["cogs.songs", "cogs.moving"]:
    try:
      await bot.load_extension(ext)
      print(f"Loaded extension: {ext}")
    except Exception as e:
      print(f"Failed to load {ext}: {e}")

@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == '__main__':
  import asyncio
  asyncio.run(setup())
  bot.run(TOKEN)
  
  #gotcha git!