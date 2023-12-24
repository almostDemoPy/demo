import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class Leaderboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /leaderboard")

  @app_commands.command(
    name = "leaderboard",
    description = "Retrieve the current leaderboard"
  )
  @app_commands.describe(
    category = "Select a leaderboard category :"
  )
  @app_commands.choices(
    category = [
      app_commands.Choice(
        name = "democoins",
        value = "democoins"
      ),
      app_commands.Choice(
        name = "arcade coins",
        value = "arcade coins"
      )
    ]
  )
  async def leaderboard(
    self,
    interaction : discord.Interaction,
    category : str
  ):
    response = interaction.response
    user = interaction.user
    await response.defer(
      thinking = True
    )
    followup = interaction.followup
    lb = get_leaderboard(category)
    if len(lb) == 0:
      err = discord.Embed(
        description = f"There currently are no leaderboard placements for category ` {category} `",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await followup.send(
        embed = embed
      )
      return
    lbTen = lb[:10]
    description = f"Here are the **Top 10** users for category ` {category} ` :\n\n"
    for ind, ID in enumerate(lbTen):
      lbUser = self.bot.get_user(ID)
      lbCategory = get_economy(ID)[category]
      if lbUser is None:
        lbUser = await self.bot.fetch_user(ID)
      description += f"`  {ind + 1} ` | {lbUser.mention} - ` {lbCategory:,} ` {category}\n"
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    userPlacement = ordinal(lb.index(str(user.id)) + 1)
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).set_footer(
      text = f"Your current placement is : {userPlacement}"
    )
    await followup.send(
      embed = embed
    )

  @leaderboard.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Leaderboard(bot))