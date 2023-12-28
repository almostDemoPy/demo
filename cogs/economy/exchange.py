import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class Exchange(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /exchange")

  @app_commands.command(
    name = "exchange",
    description = "Exchange your democoins for other currencies"
  )
  @app_commands.describe(
    currency = "Currency to exchange your democoins to",
    amount = "Amount of currency to exchange"
  )
  @app_commands.choices(
    currency = [
      app_commands.Choice(
        name = "Arcade Coins",
        value = "arcade coins"
      )
    ]
  )
  async def exchange(
    self,
    interaction : discord.Interaction,
    currency : str,
    amount : int
  ):
    response = interaction.response
    user = interaction.user
    economy = Economy(user)
    if currency == "arcade coins":
      per = 5
    if economy.democoins < per:
      err = discord.Embed(
        description = f"You don't have enough democoins ! You need ` {per:,} ` democoins to exchange for ` 1 ` {currency.capitalize()}",
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
    cost = per * amount
    if cost > economy.democoins:
      lack = cost - economy.democoins
      err = discord.Embed(
        description = f"You only have ` {economy.democoins:,} ` democoins. You need ` {lack:,} ` more to exchange for ` {amount:,} ` {currency.capitalize()}",
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
    newDemocoins = economy.subtract("democoins", cost)
    newCurrency = economy.add(currency, amount)
    embed = discord.Embed(
      description = f"Successfully exchanged currencies : ` democoins ` --> ` {currency} `",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    ).add_field(
      name = "New Democoins Balance :",
      value = f"> ` {newDemocoins:,} ` democoins",
      inline = True
    ).add_field(
      name = "Exchange Cost :",
      value = f"> ` {cost:,} ` democoins",
      inline = True
    ).add_field(
      name = f"New {currency.capitalize()} Balance :",
      value = f"> ` {newCurrency:,} ` {currency.capitalize()}",
      inline = True
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @exchange.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Exchange(bot))