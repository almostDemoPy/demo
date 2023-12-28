import discord
import random
import traceback
from discord import app_commands, ui
from discord.ext import commands

class RollADie(commands.GroupCog, name = "roll", description = "roll a die command"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /roll a die")

  a = app_commands.Group(
    name = "a",
    description = "roll a"
  )

  @a.command(
    name = "die",
    description = "Roll a die or more"
  )
  @app_commands.describe(
    count = "Amount of dice to roll",
    sides = "N-sided dice to roll"
  )
  async def rollADie(
    self,
    interaction : discord.Interaction,
    count : app_commands.Range[int, 1, 10] = 1,
    sides : app_commands.Range[int, 4, 20] = 6
  ):
    response = interaction.response
    user = interaction.user
    await response.defer(
      thinking = True,
      ephemeral = True
    )
    followup = interaction.followup
    outputs = []
    for _ in range(count):
      outputs.append(random.randint(1, sides))
    outputsTotal = sum(outputs)
    outputsStr = " | ".join([f"` {output} `" for output in outputs])
    embed = discord.Embed(
      description = f"You've rolled the dice **{count}** time(s) and got a total of ` {outputsTotal:,} ` from :\n{outputsStr}",
      color = 0x2b2d31
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await followup.send(
      embed = embed
    )

  @rollADie.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(RollADie(bot))