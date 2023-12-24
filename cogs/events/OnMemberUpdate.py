import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnMemberUpdate(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: on_member_update")

  @commands.Cog.listener()
  async def on_member_update(self, before, after):
    try:
      guild = before.guild
      if get_config(guild.id):
        config = Config(guild)
        if config.logs.on_member_update.channel_id is not None:
          channel = self.bot.get_channel(
            config.logs.on_member_update.channel_id
          )
          embed = discord.Embed(
            color = 0x2b2d31
          ).set_author(
            name = after.display_name,
            icon_url = after.display_avatar
          ).add_field(
            name = "Before :",
            value = f"""
            **Nickname** : ` {before.nickname} `
            **Avatar** : [` before `](<{before.display_avatar.url}>)
            **Roles** : {" | ".join([role.mention for role in before.roles])}
            """,
            inline = True
          ).add_field(
            name = "After :",
            value = f"""
            **Nickname** : ` {after.nickname} `
            **Avatar** : [` after `](<{after.display_avatar.url}>)
            **Roles** : {" | ".join([role.mention for role in after.roles])}
            """,
            inline = True
          )
          await channel.send(
            embed = embed
          )
    except:
      traceback.print_exc()

async def setup(bot):
  await bot.add_cog(OnMemberUpdate(bot))