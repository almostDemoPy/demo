import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class Balance(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /balance")

  @app_commands.command(
    name = "balance",
    description = 'Retrieve your current balance'
  )
  async def balance(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    economy = Economy(user)
    democoins = economy.democoins
    arcadeBalance = economy.arcades.balance
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).add_field(
      name = "Democoins",
      value = f"> ` {democoins:,} `",
      inline = True
    ).add_field(
      name = "Arcade Coins",
      value = f"> ` {arcadeBalance:,} `",
      inline = True
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @balance.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Balance(bot))