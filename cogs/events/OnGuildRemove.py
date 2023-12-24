import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnGuildRemove(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: on_guild_remove")

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    if get_config(guild.id):
      config = Config(guild)
      config.delete()

async def setup(bot):
  await bot.add_cog(OnGuildRemove(bot))