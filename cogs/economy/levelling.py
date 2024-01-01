import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class LevellingCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: levelling")

  @commands.Cog.listener()
  async def on_message(self, message):
    try:
      author = message.author
      if author.bot:
        return
      economy = Economy(author)
      economy.levelling.add(5)
      if economy.levelling.level + 1 == int(economy.levelling.experience ** ( 1 / 8)):
        economy.levelling.level_up()
        embed = discord.Embed(
          description = f"Congratulations {author.mention} ! You levelled up to ` Level {economy.levelling.level:,} ` !",
          color = 0x2b2d31
        ).set_author(
          name = self.bot.user.display_name,
          icon_url = self.bot.user.display_avatar
        )
        await message.reply(
          embed = embed,
          mention_author = False,
          delete_after = 5
        )
    except:
      traceback.print_exc()

  @app_commands.command(
    name = "level",
    description = "View your current level"
  )
  async def level(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    economy = Economy(user)
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_thumbnail(
      url = user.display_avatar
    )
    if economy.levelling.experience == 0:
      embed.add_field(
        name = "Current Ranking :",
        value = "> ` Unranked `",
        inline = True
      )
    else:
      lb = get_leaderboard("levelling")
      ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
      embed.add_field(
        name = "Current Ranking :",
        value = f"> ` {ordinal(lb.index(str(user.id)) + 1)} Place `",
        inline = True
      )
    embed.add_field(
      name = "Level :",
      value = f"> ` {economy.levelling.level:,} `",
      inline = True
    ).add_field(
      name = "Experience :",
      value = f"> ` {economy.levelling.experience:,} `",
      inline = True
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @level.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(LevellingCog(bot))