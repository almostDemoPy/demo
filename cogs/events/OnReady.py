import discord
import traceback
from discord.ext import commands

class OnReady(commands.Cog):
  def __init___(self, bot):
    self.bot = bot
    print(
      "Loaded event\t\t: on_ready()"
    )

  @commands.Cog.listener()
  async def on_ready(self):
    print(
      "demo is online"
    )

async def setup(bot):
  await bot.add_cog(OnReady(bot))