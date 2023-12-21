import discord
import random
import traceback
from discord import app_commands, ui
from discord.ext import commands

class RingTheBellView(ui.View):
  def __init__(self, user, bot):
    super().__init__(
      timeout = None
    )
    self.user = user
    self.bot = bot

  @ui.button(
    label = "🔨"
  )
  async def hammer(self, interaction, button):
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
      return
    strength = random.randint(1, 100)
    blocks = int(strength // 10)
    description = f"{user.mention} hammered down and exerted **{strength} strength**"
    if strength == 100:
      description += " and rang the bell !\n🔔 🔊\n"
    else:
      description += " !\n🔔\n"
    description += "🔳\n" * (10 - blocks)
    description += "⬜\n" * blocks
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class RingTheBell(commands.GroupCog, name = "ring", description = "ring the bell slash command"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /ring the bell")

  the = app_commands.Group(
    name = "the",
    description = "ring the bell slash command"
  )

  @the.command(
    name = "bell",
    description = "Test your strength in a game of Ring the Bell !"
  )
  async def ringTheBell(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    embed = discord.Embed(
      description = """
      Tap the hammer and give it all your strength to ring the bell !
      🔔
      🔳
      🔳
      🔳
      🔳
      🔳
      🔳
      🔳
      🔳
      🔳
      🔳
      """,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    view = RingTheBellView(user, self.bot)
    await response.send_message(
      embed = embed,
      view = view
    )

  @ringTheBell.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(RingTheBell(bot))