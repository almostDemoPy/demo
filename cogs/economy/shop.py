import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class Navigate(ui.View):
  def __init__(self, shopItems, user, bot):
    super().__init__(
      timeout = None
    )
    self.shopItems = shopItems
    self.user = user
    self.bot = bot
    self.ind = 0
    self.pos = 10 if len(shopItems) > 10 else len(shopItems)

  async def update(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    description = ""
    for item in self.shopItems[self.ind:self.pos]:
      description += f"{item}\n"
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
    emoji = "◀",
    style = discord.ButtonStyle.primary,
    disabled = True
  )
  async def previous(self, interaction, button):
    user = interaction.user
    self.ind -= 10
    if self.ind == 0:
      button.disabled = True
    else:
      button.disabled = False
    if self.pos % 10 != 0:
      self.pos -= self.pos % 10
    else:
      self.pos -= 10
    await self.update(interaction)

  @ui.button(
    emoji = "▶",
    style = discord.ButtonStyle.primary,
    disabled = False
  )
  async def next(self, interaction, button):
    user = interaction.user
    self.ind += 10
    if self.pos + 10 > len(self.shopItems):
      self.pos = len(self.shopItems)
    else:
      self.pos += 10
    await self.update(interaction)

  async def interaction_check(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    if user != self.user:
      err = discord.Embed(
        description = "This is not your menu !",
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

class Shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /shop")

  @app_commands.command(
    name = "shop",
    description = "View the shop"
  )
  @app_commands.describe(
    name = "The item to purchase",
    amount = "Amount of item to purchase"
  )
  async def shop(
    self,
    interaction : discord.Interaction,
    name : str = None,
    amount : int = 1
  ):
    response = interaction.response
    user = interaction.user
    economy = Economy(user)
    if name is not None:
      item = get_item(name)
      if item is None:
        err = discord.Embed(
          description = f"There is no such item named ` {name} `",
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
      if item.cost is None:
        err = discord.Embed(
          description = f"` {item.name} ` is not available for purchase",
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
      currency = list(item.cost.keys())[0]
      cost = item.cost[currency]
      if cost * amount > economy.currency_balance(currency):
        lack = cost * amount - economy.currency_balance(currency)
        err = discord.Embed(
          description = f"You need ` {(cost * amount):,} ` {currency} more to purchase ` {amount:,} ` **{item.name}**",
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
      economy.subtract(currency, cost * amount)
      economy.inventory.add_item(item.name, amount)
      embed = discord.Embed(
        description = f"Successfully purchased ` {amount:,} ` **{item.name}**",
        color = 0x39ff14
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      shopItems = get_shop_items()
      if not shopItems:
        err = discord.Embed(
          description = "No items are on sale right now. Come back later",
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
      else:
        pos = 10 if len(shopItems) > 10 else len(shopItems)
        description = ""
        for item in shopItems[0:pos]:
          description += f"{item}\n"
        embed = discord.Embed(
          description = description,
          color = 0x2b2d31
        ).set_author(
          name = user.display_name,
          icon_url = user.display_avatar
        )
        view = None
        if len(shopItems) > 10:
          view = Navigate(shopItems, user, self.bot)
        if view is None:
          await response.send_message(
            embed = embed
          )
        else:
          await response.send_message(
            embed = embed,
            view = view
          )

  @shop.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Shop(bot))