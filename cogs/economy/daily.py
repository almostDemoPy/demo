import discord
import traceback
from assets.db import *
from datetime import datetime, timedelta
from discord import app_commands, ui
from discord.ext import commands

class Daily(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /daily")

  @app_commands.command(
    name = "daily",
    description = "Collect your daily bonus"
  )
  @app_commands.checks.cooldown(
    1, 86400
  )
  async def daily(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    amount = 5
    economy = Economy(user)
    newBalance = economy.add(amount)
    embed = discord.Embed(
      description = f"Successfully received your daily bonus !",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    ).add_field(
      name = "New Balance :",
      value = f"> ` {newBalance:,} ` democoins",
      inline = True
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @daily.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    response = interaction.response
    if isinstance(error, app_commands.CommandOnCooldown):
      timeDiff = timedelta(
        seconds = int(error.retry_after)
      )
      timeLeft = datetime.now() + timeDiff
      err = discord.Embed(
        description = f"You can only collect your bonus every ` 24 hours `, try again <t:{int(timeLeft.timestamp())}:R>",
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
  await bot.add_cog(Daily(bot))