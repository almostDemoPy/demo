import asyncio
import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class AdminEconomy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded admin command\t: demo.economy.add")

  @commands.command(
    name = "economy.add",
    description = "Add some currency to someone"
  )
  @commands.is_owner()
  async def economyAdd(
    self,
    ctx,
    member : discord.Member,
    amount : int,
    currency : str
  ):
    author = ctx.author
    economyM = Economy(member)
    economyM.add(currency, int(amount))
    embed = discord.Embed(
      description = f"Successfully gave {member.mention} ` {amount:,} ` {currency}",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await ctx.reply(
      embed = embed,
      mention_author = False,
      delete_after = 5
    )
    await asyncio.sleep(5)
    await ctx.message.delete()

  @commands.command(
    name = "economy.subtract",
    description = "Deduct some currency from someone"
  )
  @commands.is_owner()
  async def economySubtract(
    self,
    ctx,
    member : discord.Member,
    amount : int,
    currency : str
  ):
    author = ctx.author
    economyM = Economy(member)
    economyM.subtract(currency, int(amount))
    embed = discord.Embed(
      description = f"Successfully deducted ` {amount:,} ` {currency} from {member.mention}",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await ctx.reply(
      embed = embed,
      mention_author = False,
      delete_after = 5
    )
    await asyncio.sleep(5)
    await ctx.message.delete()

  @economyAdd.error
  @economySubtract.error
  async def error(self, ctx, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(AdminEconomy(bot))