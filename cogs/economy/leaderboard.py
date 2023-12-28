import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands, tasks

class GlobalLeaderboardView(ui.View):
  def __init__(self, bot, democoins, arcadeCoins):
    super().__init__(
      timeout = None
    )
    self.bot = bot
    self.children[0].disabled = democoins
    self.children[1].disabled = arcadeCoins

  @ui.button(
    label = "Democoins Leaderboard Placement",
    row = 0
  )
  async def demoCoinsLbPlacement(self, interaction, button):
    response = interaction.response
    user = interaction.user
    if get_eco(user.id)["democoins"] == 0:
      err = discord.Embed(
        description = "You don't have a placement in the ` democoins ` global leaderboard",
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
    lb = get_leaderboard("democoins")
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    userPlacement = ordinal(lb.index(str(user.id)) + 1)
    if userPlacement == "1st":
      ind2 = 0
    elif userPlacement == "2nd":
      ind2 = 1
    else:
      ind2 = 2
    if lb.index(str(user.id)) + 1 == len(lb):
      pass
    lb2 = []
    for ind, ID in enumerate(lb[ind2:]):
      if len(lb2) == 5:
        break
      lbCategory = get_eco(ID)["democoins"]
      if lbCategory == 0:
        continue
      lb2.append(ID)
    lb5 = lb2
    description = f"Here is your global leaderboard placement for category ` democoins ` :\n\n"
    for ind, ID in enumerate(lb5):
      lbUser = self.bot.get_user(ID)
      lbCategory = get_eco(ID)["democoins"]
      if lbCategory == 0:
        continue
      if lbUser is None:
        lbUser = await self.bot.fetch_user(ID)
      description += f"`  {ind + 1} ` | {lbUser.mention} - ` {lbCategory:,} ` democoins\n"
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @ui.button(
    label = "Arcade Coins Leaderboard Placement",
    row = 1
  )
  async def arcadeCoinsLbPlacement(self, interaction, button):
    response = interaction.response
    user = interaction.user
    if get_eco(user.id)["democoins"] == 0:
      err = discord.Embed(
        description = "You don't have a placement in the ` arcade coins ` global leaderboard",
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
    lb = get_leaderboard("arcade coins")
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    userPlacement = ordinal(lb.index(str(user.id)) + 1)
    if userPlacement == "1st":
      ind2 = 0
    elif userPlacement == "2nd":
      ind2 = 1
    else:
      ind2 = 2
    if lb.index(str(user.id)) + 1 == len(lb):
      pass
    lb2 = []
    for ind, ID in enumerate(lb[ind2:]):
      if len(lb2) == 5:
        break
      lbCategory = get_eco(ID)["arcade coins"]
      if lbCategory == 0:
        continue
      lb2.append(ID)
    lb5 = lb2
    description = f"Here is your global leaderboard placement for category ` arcade coins ` :\n\n"
    for ind, ID in enumerate(lb5):
      lbUser = self.bot.get_user(ID)
      lbCategory = get_eco(ID)["arcade coins"]
      if lbCategory == 0:
        continue
      if lbUser is None:
        lbUser = await self.bot.fetch_user(ID)
      description += f"`  {ind + 1} ` | {lbUser.mention} - ` {lbCategory:,} ` arcade coins\n"
    embed = discord.Embed(
      description = description,
      color = 0x2b2d31
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  async def interaction_check(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    if not get_economy(user.id):
      err = discord.Embed(
        description = "You do not have a data in ` ECONOMY ` database",
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

class Leaderboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.globalLeaderboardChannel = self.bot.get_channel(1189420111942139924)
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
    guild = interaction.guild
    await response.defer(
      thinking = True
    )
    followup = interaction.followup
    lb = get_leaderboard(category)
    lb = [u for u in lb if guild.get_member(int(u)) is not None]
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
      lbCategory = get_eco(ID)[category]
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

  @commands.Cog.listener()
  async def on_ready(self):
    if self.globalLeaderboardChannel is None:
      self.globalLeaderboardChannel = self.bot.get_channel(1189420111942139924)
    if not self.globalLeaderboard.is_running():
      self.globalLeaderboard.start()

  @tasks.loop(
    hours = 1
  )
  async def globalLeaderboard(self):
    try:
      lbEmbed = None
      channel = self.globalLeaderboardChannel
      demoCoinsLb = get_leaderboard("democoins")
      arcadeCoinsLb = get_leaderboard("arcade coins")
      ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
      democoins = False
      arcadeCoins = False
      if len(demoCoinsLb) == 0:
        embed1 = discord.Embed(
          description = f"There currently are no leaderboard placements for category ` democoins `",
          color = 0xff3131
        )
        democoins = True
      else:
        lbTen = demoCoinsLb[:10]
        description = f"Here are the **Top 10** users for category ` democoins ` :\n\n"
        for ind, ID in enumerate(lbTen):
          lbUser = self.bot.get_user(ID)
          lbCategory = get_eco(ID)["democoins"]
          if lbCategory == 0:
            continue
          if lbUser is None:
            lbUser = await self.bot.fetch_user(ID)
          description += f"`  {ind + 1} ` | {lbUser.mention} - ` {lbCategory:,} ` democoins\n"
        embed1 = discord.Embed(
          description = description,
          color = 0x2b2d31
        )
      if len(arcadeCoinsLb) == 0:
        embed2 = discord.Embed(
          description = f"There currently are no leaderboard placements for category ` arcade coins `",
          color = 0xff3131
        )
        arcadeCoins = True
      else:
        lbTen = arcadeCoinsLb[:10]
        description = f"Here are the **Top 10** users for category ` arcade coins ` :\n\n"
        for ind, ID in enumerate(lbTen):
          lbUser = self.bot.get_user(ID)
          lbCategory = get_eco(ID)["arcade coins"]
          if lbCategory == 0:
            continue
          if lbUser is None:
            lbUser = await self.bot.fetch_user(ID)
          description += f"`  {ind + 1} ` | {lbUser.mention} - ` {lbCategory:,} ` arcade coins\n"
        embed2 = discord.Embed(
          description = description,
          color = 0x2b2d31
        )
      msgID = get_data("global leaderboard message")
      if msgID is None:
        message = await channel.send(
          embeds = [
            embed1,
            embed2
          ],
          view = GlobalLeaderboardView(
            self.bot,
            democoins,
            arcadeCoins
          )
        )
        update_data("global leaderboard message", message.id)
      else:
        msg = await channel.fetch_message(msgID)
        await msg.edit(
          embeds = [
            embed1,
            embed2
          ],
          view = GlobalLeaderboardView(
            self.bot,
            democoins,
            arcadeCoins
          )
        )
    except:
      traceback.print_exc()

  @leaderboard.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Leaderboard(bot))