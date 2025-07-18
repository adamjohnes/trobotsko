import discord
from discord.ext import commands
import asyncio
from classes.Playlist import Playlist
from util.db import create_playlist_db

class Playlists(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="create-pl", help='creates a playlist of saved songs for user [<create-pl "favSongs"]')
  async def create_playlist(self, ctx, *, name: str):
    try:
      newPlaylist = Playlist()
      await newPlaylist.create_playlist(ctx, name)
      loop = ctx.bot.loop
      await loop.run_in_executor(
        None,
        create_playlist_db,
        self.bot.db_pool,
        ctx.author,
        name
      )
    except Exception as e:
      await ctx.send("Error creating playlist.")
      print(e)

  @commands.command(name="add-song", help="adds a song to the playlist [<add-song favSongs the hell song]")
  async def add_song(self, ctx, *, songElement):
    try:
      pass
    except Exception as e:
      await ctx.send("Error adding song to playlist.")
      print(e)

async def setup(bot):
  await bot.add_cog(Playlists(bot))
