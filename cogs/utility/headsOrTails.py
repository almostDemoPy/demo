import discord
import random
import traceback
from discord import app_commands, ui
from discord.ext import commands

class HeadsOrTails(commands.GroupCog, name = "heads", description = "Heads or Tails command"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command : /heads or tails")

  Or = app_commands.Group(
    name = "or",
    description = "heads or tails command"
  )

  @Or.command(
    name = "tails",
    description = "Flip a coin and test your luck"
  )
  @app_commands.describe(
    heads = "the option for heads",
    tails = "the option for tails"
  )
  async def headsOrTails(self, interaction : discord.Interaction, heads : str, tails : str):
    response = interaction.response
    user = interaction.user
    botChoice = random.choice(["Heads", "Tails"])
    if botChoice == "Heads":
      selectedOption = heads
    elif botChoice == "Tails":
      selectedOption = tails
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).add_field(
      name = "Heads :",
      value = f"> {heads}",
      inline = True
    ).add_field(
      name = "Tails :",
      value = f"> {tails}",
      inline = True
    ).add_field(
      name = f"Selected : {botChoice}",
      value = f"> {selectedOption}",
      inline = False
    )
    await response.send_message(
      embed = embed
    )

  @headsOrTails.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(HeadsOrTails(bot))