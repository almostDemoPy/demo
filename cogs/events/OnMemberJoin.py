import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnMemberJoin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: on_member_join")

  @commands.Cog.listener()
  async def on_member_join(self, member):
    try:
      guild = member.guild
      if get_config(guild.id):
        config = Config(guild)
        if config.welcome.channel_id is not None:
          channel = self.bot.get_channel(config.welcome.channel_id)
          embed = discord.Embed(
            description = config.welcome.description.replace("{member.mention}", member.mention).replace("{guild.name}", guild.name),
            color = 0x2b2d31
          ).set_author(
            name = guild.owner.display_name,
            icon_url = guild.owner.display_avatar
          ).set_thumbnail(
            url = member.display_avatar
          )
          await channel.send(
            embed = embed
          )
    except:
      traceback.print_exc()

async def setup(bot):
  await bot.add_cog(OnMemberJoin(bot))