import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class ItemCommands(commands.GroupCog, name = "item", description = "item commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /item user")


  @app_commands.command(
    name = "use",
    description = "Use an item from your inventory"
  )
  @app_commands.describe(
    item = "Item to user",
    amount = "Amount of item to use",
    member = "Member to use the item on"
  )
  async def itemUse(
    self,
    interaction : discord.Interaction,
    item : str,
    member : discord.Member = None,
    amount : int = 1
  ):
    response = interaction.response
    user = interaction.user
    economy = Economy(user)
    if get_item(item) is None:
      err = discord.Embed(
        description = f"There is no such item named ` {item} `",
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
    item = Item(item)
    await item.execute(interaction, member, amount)

  @app_commands.command(
    name = "info",
    description = "Retrieve the info of an item"
  )
  @app_commands.describe(
    name = "Name of an item"
  )
  async def itemInfo(
    self,
    interaction : discord.Interaction,
    name : str
  ):
    response = interaction.response
    user = interaction.user
    if get_item(name) is None:
      err = discord.Embed(
        description = f"There is no such item named ` {name} `",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embeed = err,
        ephemeral = True
      )
      return
    item = Item(name)
    embed = discord.Embed(
      title = item.name,
      description = f"""
> {item.description}
      """,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    )
    if item.cost is not None:
      embed.add_field(
        name = "Cost :",
        value = f"> ` {item.cost[list(item.cost.keys())[0]]} ` {list(item.cost.keys())[0]}",
        inline = True
      )
    embed.add_field(
      name = "Useable :",
      value = f"> ` {str(item.useable).capitalize()} `",
      inline = True
    ).add_field(
      name = "Sellable :",
      value = f"> ` {str(item.sellable).capitalize()} `",
      inline = True
    )
    await response.send_message(
      embed = embed
    )

  @itemUse.error
  @itemInfo.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(ItemCommands(bot))