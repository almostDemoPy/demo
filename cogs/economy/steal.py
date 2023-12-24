import discord
import random
import traceback
from assets.db import *
from datetime import datetime, timedelta
from discord import app_commands, ui
from discord.ext import commands

class Steal(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /steal")

  @app_commands.command(
    name = "steal",
    description = "Steal democoins from another member"
  )
  @app_commands.describe(
    member = "Member to steal from"
  )
  @app_commands.checks.cooldown(
    1, 300
  )
  async def steal(
    self,
    interaction : discord.Interaction,
    member : discord.Member
  ):
    response = interaction.response
    user = interaction.user
    if member.bot:
      err = discord.Embed(
        description = "You cannot steal from a bot",
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
    if economyM.democoins == 0:
      err = discord.Embed(
        description = "This member has no democoins !",
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
    if not random.choice([False, False, False, False, True]):
      err = discord.Embed(
        description = f"You tried to steal from {member.mention} but failed, how unfortunate",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      embed = discord.Embed(
        description = f"{user.mention} tried to steal from you but failed",
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await member.send(
        embed = embed
      )
      return
    stolen = random.randint(1, economyM.democoins)
    percentage = (stolen / economyM.democoins) * 100
    newBalance = economyU.add(stolen)
    economyM.subtract(stolen)
    embed = discord.Embed(
      description = f"Successfully stole **{percentage} %%** of {member.mention}'s democoins",
      color = 0x39ff14
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).add_field(
      name = "New Balance :",
      value = f"> ` {newBalance:,} ` democoins",
      inline = True
    ).add_field(
      name = "Amount Stolen :",
      value = f"> ` {stolen:,} ` democoins",
      inline = True
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )
    embed = discord.Embed(
      description = f"Someone just stole ` {stolen:,} ` democoins from you",
      color = 0x2b2d31
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await member.send(
      embed = embed
    )

  @steal.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    response = interaction.response
    if isinstance(error, app_commands.CommandOnCooldown):
      timeDiff = timedelta(
        seconds = int(error.retry_after)
      )
      timeLeft = datetime.now() + timeDiff
      err = discord.Embed(
        description = f"You can only steal from someone every ` 5 minutes `, try again <t:{int(timeLeft.timestamp())}:R>",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )

async def setup(bot):
  await bot.add_cog(Steal(bot))