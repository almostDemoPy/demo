import discord
import traceback
from db import *
from discord import app_commands, ui
from discord.ext import commands

class GuildConfig(commands.GroupCog, name = "config", description = "guild config commands"):
  def __init__(self, bot):
    self.bot = bot

  channel = app_commands.Group(
    name = "channel",
    description = "guild config channel commands"
  )

  @channel.command(
    name = "welcome",
    description = "Configure this guild's welcome channel"
  )
  @app_commands.describe(
    channel = "Channel to set it to"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  async def configChannelWelcome(self, interaction : discord.Interaction, channel : discord.TextChannel = None):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != guild.owner:
      err = discord.Embed(
        description = "Only the Guild Owner can execute this command",
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
    config = Config(guild)
    if channel is None:
      if config.welcome.channel_id is None:
        err = discord.Embed(
          description = "` Welcome Channel ` is already set to ` None `",
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
      embed = discord.Embed(
        description = f"Successfully set ` Welcome Channel ` to : ` None `",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      config.welcome.clear()
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      embed = discord.Embed(
        description = f"Successfully set ` Welcome Channel ` to : {channel.mention}",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      config.welcome.update(channel)
      await response.send_message(
        embed = embed,
        ephemeral = True
      )

  @configChannelWelcome.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(GuildConfig(bot))