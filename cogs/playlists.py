import discord
from discord.ext import commands
import asyncio
from classes.Playlist import Playlist
from util.db import create_playlist_db, select_playlist_db, insert_song_db
from util.song_utils import determine_message_type
import shlex
import json

class Playlists(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="create-pl", help='creates a playlist of saved songs [<create-pl "favSongs"]')
  async def create_playlist_command(self, ctx, *, name: str):
    results = await see_playlists_todb(self.bot, ctx)
    await initialize_playlist_todb(self.bot, ctx, name=name, results=results)

  @commands.command(name="add-song", help='adds song to a playlist [<add-song "favSongs" the hell song]')
  async def add_song_command(self, ctx, *, songElement: str):
    results = await see_playlists_todb(self.bot, ctx)
    await get_playlist_and_song(self.bot, ctx, songElement=songElement, results=results)
    
  @commands.command(name="see-pl", help='shows playlists of user')
  async def see_playlists_command(self, ctx):
    results = await see_playlists_todb(self.bot, ctx)
    await ctx.send(f"{results}")
    
#to-do prevent duplicately named playlists! (atleast per unique id)
async def see_playlists_todb(bot, ctx):
  try:
    loop = ctx.bot.loop
    results = await loop.run_in_executor(
      None,
      select_playlist_db,
      bot.db_pool,
      ctx.author
    )
    return results
  except Exception as e:
    print(e)

async def initialize_playlist_todb(bot, ctx, *, name: str, results):
  try:
    # grab headers (playlist names)
    lines = results.strip().splitlines()
    headers = [line.split(":", 1)[0].strip('"').lower() for line in lines if ":" in line]
    
    newPlaylist = Playlist()
    await newPlaylist.create_playlist(ctx, name)
    
    playlistName = name.lower().strip('"')   
     
    if playlistName in headers:
      await ctx.send(f"Playlist: {name} already exists. Use <see-pl to view your playlists.")
      return   
    
    loop = ctx.bot.loop  
    await loop.run_in_executor(
      None,
      create_playlist_db,
      bot.db_pool,
      ctx.author,
      name
    )
    
    await ctx.send(f"New playlist created: {name}")
  except Exception as e:
    await ctx.send("Error creating playlist.")
    print(e)

# force all lowercase
# add insert logic
async def get_playlist_and_song(bot, ctx, *, songElement: str, results):
  try:
    arguments = shlex.split(songElement)

    if len(arguments) < 2:
      await ctx.send(
        'When calling <add-song, please provide ["playlist"] followed by [title] '
        '(i.e. <add-song "my favorite playlist" star spangled banner)'
      )
      return

    playlist_name = arguments[0].lower()
    song_title = " ".join(arguments[1:])

    # check if playlist exists (using headers from DB result)
    lines = results.strip().splitlines()
    headers = [line.split(":", 1)[0].strip('"').lower() for line in lines if ":" in line]

    if playlist_name not in headers:
      await ctx.send(f"Playlist: {playlist_name} doesn't exist. Use command <see-pl to check your playlists.")
      return

    # determine song info
    song = await determine_message_type(song_title)
    song_dict = song.to_dict()

    # Insert into DB
    loop = ctx.bot.loop
    await loop.run_in_executor(
      None,
      insert_song_db,
      bot.db_pool,
      ctx.author,
      '"' + arguments[0] + '"',
      song_dict
    )

    await ctx.send(f'Added **{song.title}** to **"{playlist_name}"**.')

  except Exception as e:
    print(e)
    await ctx.send(
      'Error adding song to playlist. Use format: <add-song "playlist name" song title'
    )

    
async def setup(bot):
  await bot.add_cog(Playlists(bot))
