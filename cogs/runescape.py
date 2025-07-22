from discord.ext import commands
from util.db import *

class Runescape(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="rsn", help="insert/update your OSRS RSN")
  async def set_rsn(self, ctx, *, rsn: str):
    loop = ctx.bot.loop
    await loop.run_in_executor(
      None,
      perform_query,
      self.bot.db_pool,
      f"[DB] Updating RSN for {ctx.author.id} → {rsn}",
      "UPDATE users SET rsn=%s WHERE id=%s",
      (rsn, ctx.author.id)
    )
    await ctx.send(f"Your RSN has been updated to **{rsn}**!")

async def setup(bot):
  await bot.add_cog(Runescape(bot))