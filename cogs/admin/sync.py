import asyncio
import discord
import traceback
from discord.ext import commands

class Sync(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(
      "Loaded command : demo.sync"
    )

  @commands.command(
    name = "sync",
    description = "Sync all interaction commands"
  )
  @commands.is_owner()
  async def sync(self, ctx):
    await ctx.bot.tree.sync()
    embed = discord.Embed(
      description = "All interaction commands have been successfully synced",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await ctx.reply(
      embed = embed,
      mention_author = False,
      delete_after = 10
    )
    await asyncio.sleep(10)
    await ctx.message.delete()

  @sync.error
  async def error(self, ctx, error):
    traceback.print_exc()
    err = discord.Embed(
      description = "Something went wrong. Try again later",
      color = 0xff3131
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await ctx.reply(
      embed = err,
      mention_author = False,
      delete_after = 10
    )
    await asyncio.sleep(10)
    await ctx.message.delete()

async def setup(bot):
  await bot.add_cog(Sync(bot))