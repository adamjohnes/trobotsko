import discord
from discord.ext import commands
import asyncio
from classes.Playlist import Playlist
from util.db import create_playlist_db
from util.song_utils import determine_message_type
import shlex

class Playlists(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="create-pl", help='creates a playlist of saved songs [<create-pl "favSongs"]')
  async def create_playlist(self, ctx, *, name: str):
    initialize_playlist_todb(self.bot, ctx, name)

  @commands.command(name="add-song", help='adds song to a playlist [<add-song "favSongs" the hell song]')
  async def add_song(self, ctx, *, songElement: str):
    get_playlist_and_song(songElement)
    

async def initialize_playlist_todb(bot, ctx, *, name: str):
  try:
    newPlaylist = Playlist()
    await newPlaylist.create_playlist(ctx, name)
    loop = ctx.bot.loop
    await loop.run_in_executor(
      None,
      create_playlist_db,
      bot.db_pool,
      ctx.author,
      name
    )
  except Exception as e:
    await ctx.send("Error creating playlist.")
    print(e)

async def get_playlist_and_song(ctx, *, songElement: str)
  try:
    arguments = shlex.split(songElement)
    if len(arguments) < 2:
      await ctx.send('When calling <add-song, please provide ["playlist"] followed by [title] (i.e. <add-song "my favorite playlist" star spangled banner)')
    else:
      playlistName = arguments[0]
      songTitle = " ".join(arguments[1:])
      song = await determine_message_type(songTitle)
      await ctx.send(f'Adding **{song.title}** to **"{playlistName}"**')
  except Exception as e:
    await ctx.send('Error adding song to playlist. When calling <add-song, please provide ["playlist"] followed by [title] (i.e. <add-song "my favorite playlist" star spangled banner)')
    print(e)
    
async def setup(bot):
  await bot.add_cog(Playlists(bot))
