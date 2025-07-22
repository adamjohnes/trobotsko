import discord
from discord.ext import commands
import asyncio
from util.db import create_playlist_db, select_playlist_db, insert_song_db, remove_song_db
from util.song_utils import determine_message_type
import shlex
import json
from datetime import datetime
from classes.SongQueue import SongQueue
from classes.Playlist import Playlist

class Playlists(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="create-pl", help='creates an empty song playlist [<create-pl favSongs]')
  async def create_playlist_command(self, ctx, *, playlistName: str):
    results = await see_playlists_fromdb(self.bot, ctx)
    await initialize_playlist_todb(self.bot, ctx, playlistName=playlistName, results=results)

  @commands.command(name="add-song", help='adds song to a playlist [<add-song favSongs the hell song]')
  async def add_song_command(self, ctx, *, songElement: str):
    results = await see_playlists_fromdb(self.bot, ctx)
    await insert_song_todb(self.bot, ctx, songElement=songElement, results=results)
    
  @commands.command(name="remove-song", help='removes song from playlist [<remove-song favSongs Yeah 3x]')
  async def remove_song_command(self, ctx, *, songElement: str):
    results = await see_playlists_fromdb(self.bot, ctx)
    await remove_song_fromdb(self.bot, ctx, songElement=songElement, results=results)
    
  @commands.command(name="use-pl", help='select a playlist to play songs from [<use-pl favSongs]')
  async def use_playlist_command(self, ctx, *, playlistName: str):
    results = await see_playlists_fromdb(self.bot, ctx)
    await use_playlist(self.bot, ctx, playlistName=playlistName, results=results)
    
  @commands.command(name="see-pl", help='shows playlists of user')
  async def see_playlists_command(self, ctx):
    results = await see_playlists_fromdb(self.bot, ctx)
    await ctx.send(f"**{ctx.author.name}**'s playlists:\n```json\n{json.dumps(results, indent=2)}```")

async def use_playlist(bot, ctx, playlistName, results):
  try:
    # grab headers (playlist names)
    playlists = results.keys()
     
    if playlistName not in playlists:
      await ctx.send(f"Playlist: {playlistName} does not exist. Use <see-pl to view your playlists.")
      return
  
    print(results)
    for playlist, songs in results.items():
      if (playlist == playlistName):
        for song in songs:
          try:
            bot.Trobotsko.songList.push_song(await determine_message_type(song["title"]))
          except Exception as e:
            print(e)
        
  except Exception as e:
    print(e)

async def see_playlists_fromdb(bot, ctx):
  try:
    loop = ctx.bot.loop
    results = await loop.run_in_executor(
      None,
      select_playlist_db,
      bot.db_pool,
      ctx.author
    )
    
    if not results:
      return f"User: {ctx.author.name} does not have any playlists."
    
    return results
  except Exception as e:
    print(e)

async def initialize_playlist_todb(bot, ctx, *, playlistName: str, results):
  try:
    # grab headers (playlist names)
    playlists = results.keys()
     
    if playlistName in playlists:
      await ctx.send(f"Playlist: {playlistName} already exists. Use <see-pl to view your playlists.")
      return   
    
    loop = ctx.bot.loop  
    await loop.run_in_executor(
      None,
      create_playlist_db,
      bot.db_pool,
      ctx.author,
      playlistName.strip('"')
    )
    
    await ctx.send(f"New playlist created: {playlistName}")
  except Exception as e:
    await ctx.send("Error creating playlist.")
    print(e)

# force all lowercase
# add insert logic
async def insert_song_todb(bot, ctx, *, songElement: str, results):
  try:
    arguments = shlex.split(songElement)

    if len(arguments) < 2:
      await ctx.send(
        '***When calling <add-song, please provide [playlist] followed by [title] '
        '(i.e. <add-song my favorite playlist star spangled banner)***'
      )
      return

    playlist_name = arguments[0].lower()
    song_title = " ".join(arguments[1:])

    # check if playlist exists (using headers from DB result)
    playlists = results.keys()

    if playlist_name not in playlists:
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
      arguments[0],
      song_dict
    )

    await ctx.send(f'Added **{song.title}** to **"{playlist_name}"**.')

  except Exception as e:
    print(e)
    await ctx.send(
      '***Error adding song to playlist. Please use [playlist] followed by [title] '
        '(i.e. <add-song my favorite playlist star spangled banner)***'
    )
    
async def remove_song_fromdb(bot, ctx, *, songElement: str, results):
  try:
    arguments = shlex.split(songElement)

    if len(arguments) < 2:
      await ctx.send(
        '***When calling <remove-song, please provide [playlist] followed by [title] '
        '(i.e. <remove-song my favorite playlist star spangled banner)***'
      )
      return

    playlist_name = arguments[0].lower()
    song_title = " ".join(arguments[1:])

    # check if playlist exists (using headers from DB result)
    playlists = results.keys()

    if playlist_name not in playlists:
      await ctx.send(f"Playlist: {playlist_name} doesn't exist. Use command <see-pl to check your playlists.")
      return
    
    song = await determine_message_type(song_title)
    
    song_dict = song.to_dict()
    
    # Remove from DB
    loop = ctx.bot.loop
    success = await loop.run_in_executor(
      None,
      remove_song_db,
      bot.db_pool,
      ctx.author,
      arguments[0],
      song_dict
    )
    if success:
      await ctx.send(f"```{song} successfully removed from **{playlist_name}**.```")
    else:
      await ctx.send(f"```{song} was not found in **{playlist_name}**.```")
  except Exception as e:
    print(e)
    await ctx.send(
      '***Error adding song to playlist. Please use ["playlist"] followed by [title] '
        '(i.e. <add-song "my favorite playlist" star spangled banner)***'
    )
    
async def setup(bot):
  await bot.add_cog(Playlists(bot))
