import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from classes.BotAPI import BotAPI
import logging
from datetime import date

logs_directory = "C:\\Users\\owner\\Documents\\vsc\\misc\\python\\trobotsko\\logs\\"

logging.basicConfig(
  filename=f"{logs_directory}trobotsko_logs_{str(date.today())}.log",
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(message)s",
  encoding="utf-8"
)

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trobotsko = None  # Ensure attribute exists

    async def setup_hook(self):
        self.Trobotsko = BotAPI()
        for ext in ["cogs.songs", "cogs.moving"]:
            try:
                await self.load_extension(ext)
                print(f"Loaded extension: {ext}")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")

intents = discord.Intents.all()
bot = MyBot(command_prefix='<', intents=intents)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down.")
    await bot.close()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    logging.info(f"Trobotsko: {message.content}")
  else:
    logging.info(f"User[{message.author}]: {message.content}")
  await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
  logging.error(f"Error using command: {ctx.command}: {error}")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)