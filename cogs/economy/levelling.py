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
      economy = Economy(author)
      economy.add(5)
      if economy.levelling.level == int(economy.levelling.experience ** ( 1 / 8)):
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

async def setup(bot):
  await bot.add_cog(LevellingCog(bot))