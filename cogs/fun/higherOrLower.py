import discord
import random
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class HOL(ui.View):
  def __init__(self, user, num, hint, bot):
    super().__init__(
      timeout = None
    )
    self.user = user
    self.num = num
    self.hint = hint
    self.economy = Economy(user)
    self.bot = bot

  async def game(self, interaction : discord.Interaction, guess):
    response = interaction.response
    user = interaction.user
    win = False
    if guess == "lower" and self.num < self.hint:
      win = True
    elif guess == "jackpot" and self.num == self.hint:
      win = True
    elif guess == "higher" and self.num > self.hint:
      win = True
    if win:
      embed = discord.Embed(
        description = f"""You guessed **right** !""",
        color = 0x39ff14
      )
    else:
      embed = discord.Embed(
        description = f"""You guessed **wrong** !""",
        color = 0xff3131
      )
    embed.add_field(
      name = "Hint :",
      value = f"> ` {self.hint} `",
      inline = True
    ).add_field(
      name = "Number :",
      value = f"> ` {self.num} `",
      inline = True
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  @ui.button(
    emoji = "🔽"
  )
  async def lower(self, interaction, button):
    await self.game(interaction, "lower")

  @ui.button(
    emoji = "💎"
  )
  async def jackpot(self, interaction, button):
    await self.game(interaction, "jackpot")

  @ui.button(
    emoji = "🔼"
  )
  async def higher(self, interaction, button):
    await self.game(interaction, "higher")

  async def interaction_check(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    if user != self.user:
      err = discord.Embed(
        description = "This is not your game !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return False
    return True

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class HigherOrLower(commands.GroupCog, name = "higher", description = "/higher or lower command"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /higher or lower")

  _or = app_commands.Group(
    name = "or",
    description = "higher or"
  )

  @_or.command(
    name = "lower",
    description = "Play a game of Higher or Lower !"
  )
  async def higherOrLower(
    self,
    interaction : discord.Interaction
  ):
    response = interaction.response
    user = interaction.user
    num = random.randint(1, 100)
    hint = random.randint(1, 100)
    embed = discord.Embed(
      description = f"I chose a number from **1** to **100**.\nYour number is **{hint}**.\nIs my number ` higher ` or ` lower ` than yours ?",
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    view = HOL(user, num, hint, self.bot)
    await response.send_message(
      embed = embed,
      view = view
    )

  @higherOrLower.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(HigherOrLower(bot))