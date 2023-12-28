import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class Navigate(ui.View):
  def __init__(self, items, user, bot):
    super().__init__(
      timeout = None
    )
    self.items = items
    self.ind = 0
    self.pos = 10
    self.user = user
    self.bot = bot

  @ui.button(
    emoji = "◀",
    style = discord.ButtonStyle.primary,
    disabled = True
  )
  async def previous(self, interaction, button):
    response = interaction.response
    user = interaction.user
    self.ind -= 10
    if self.pos % 10 != 0:
      self.pos -= self.pos % 10
    else:
      self.pos -= 10
    button.disabled = True if self.ind == 0 else False
    self.children[1].disabled = False
    description = ""
    for item, amount in self.items[self.ind:self.pos]:
      description += f"**{item}** - ` {amount:,} `\n"
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    await response.edit_message(
      embed = embed,
      view = self
    )

  @ui.button(
    emoji = "▶",
    style = discord.ButtonStyle.primary,
    disabled = False
  )
  async def next(self, interaction, button):
    response = interaction.response
    user = interaction.user
    self.ind += 10
    if self.pos + 10 > len(self.items):
      self.pos = len(self.items)
    else:
      self.pos += 10
    button.disabled = True if self.pos == len(self.items) else False
    self.children[0].disabled = False
    description = ""
    for item, amount in self.items[self.ind:self.pos]:
      description += f"**{item}** - ` {amount:,} `\n"
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    await response.edit_message(
      embed = embed,
      view = self
    )

  async def interaction_check(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    if user != self.user:
      err = discord.Embed(
        description = "This is not your inventory !",
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

class Inventory(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /inventory")

  @app_commands.command(
    name = "inventory",
    description = "Check your inventory"
  )
  @app_commands.describe(
    item = "Item to check"
  )
  async def inventory(self, interaction : discord.Interaction, item : str = None):
    response = interaction.response
    user = interaction.user
    economy = Economy(user)
    if not economy.inventory.items:
      err = discord.Embed(
        description = "You currently have no items in your inventory",
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
    items = economy.inventory.items
    pos = 10 if len(items) > 10 else len(items)
    description = ""
    for item, amount in items[0:pos]:
      description += f"**{item}** - ` {amount:,} `\n"
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    view = None
    if len(items) > 10:
      view = Navigate(items, user, self.bot)
    if view is None:
      await response.send_message(
        embed = embed
      )
    else:
      await response.send_message(
        embed = embed,
        view = view
      )

  @inventory.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Inventory(bot))