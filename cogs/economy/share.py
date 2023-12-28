import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class Share(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /share")

  @app_commands.command(
    name = "share",
    description = "Share some democoins to your friends !"
  )
  @app_commands.describe(
    member = "To whom you'll share the democoins to",
    amount = "Amount to share"
  )
  async def share(
    self,
    interaction : discord.Interaction,
    member : discord.Member,
    amount : int
  ):
    response = interaction.response
    user = interaction.user
    if member.bot:
      err = discord.Embed(
        description = "You cannot share coins with a bot",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    economyU = Economy(user)
    economyM = Economy(member)
    if amount > economyU.democoins:
      err = discord.Embed(
        description = f"You can only send up to ` {economyU.democoins:,} ` democoins !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if amount < 0:
      err = discord.Embed(
        description = f"You must send at least ` 0 ` and at most ` {economyU.democoins:,} ` democoins !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    newBalanceU = economyU.subtract("democoins", amount)
    newBalanceM = economyM.add("democoins", amount)
    embed = discord.Embed(
      description = f"Successfully gave {member.mention} ` {amount:,} ` democoins",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    ).add_field(
      name = "New Balance :",
      value = f"> ` {newBalanceU:,} ` democoins",
      inline = True
    ).add_field(
      name = f"{member.display_name}'s New Balance :",
      value = f"> ` {newBalanceM:,} ` democoins",
      inline = True
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @share.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Share(bot))