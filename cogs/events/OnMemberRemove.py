import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnMemberRemove(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def on_member_remove(self, member):
    try:
      guild = member.guild
      if get_config(guild.id):
        config = Config(guild)
        if config.farewell.channel_id is not None:
          channel = self.bot.get_channel(config.farewell.channel_id)
          embed = discord.Embed(
            description = config.farewell.description.replace("{member.mention}", member.mention).replace("{guild.name}", guild.name),
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
  await bot.add_cog(OnMemberRemove(bot))