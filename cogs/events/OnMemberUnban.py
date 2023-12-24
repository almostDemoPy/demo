import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnMemberUnban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: on_member_unban")

  @commands.Cog.listener()
  async def on_member_unban(self, guild, member):
    try:
      if get_config(guild.id):
        config = Config(guild)
        if config.logs.on_member_ban.channel_id is not None:
          channel = self.bot.get_channel(
            config.logs.on_member_unban.channel_id
          )
          embed = discord.Embed(
            description = f"User ` {member.name} ( {member.id} ) ` has been unbanned from this guild",
            color = 0x2b2d31
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          ).set_thumbnail(
            url = member.display_avatar
          )
          await channel.send(
            embed = embed
          )
    except:
      traceback.print_exc()

async def setup(bot):
  await bot.add_cog(OnMemberUnban(bot))