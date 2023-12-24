import discord
import traceback
from assets.db import *
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

  @channel.command(
    name = "farewell",
    description = "Configure this guild's farewell channel"
  )
  @app_commands.describe(
    channel = "Channel to set it to"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  async def configChannelFarewell(self, interaction : discord.Interaction, channel : discord.TextChannel = None):
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
      if config.farewell.channel_id is None:
        err = discord.Embed(
          description = "` Farewell Channel ` is already set to ` None `",
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
        description = f"Successfully set ` Farewell Channel ` to : ` None `",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      config.farewell.clear()
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      embed = discord.Embed(
        description = f"Successfully set ` Farewell Channel ` to : {channel.mention}",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      config.farewell.update(channel)
      await response.send_message(
        embed = embed,
        ephemeral = True
      )

  @channel.command(
    name = "logs",
    description = "Configure this guild's logs channel"
  )
  @app_commands.describe(
    channel = "Channel to set it to",
    action = "Logs action to configure"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  @app_commands.choices(
    action = [
      app_commands.Choice(
        name = "OnMessageEdit",
        value = "OnMessageEdit"
      )
    ]
  )
  async def configChannelLogs(
    self,
    interaction : discord.Interaction,
    action : str,
    channel : discord.TextChannel = None
  ):
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
      if config.logs.get(action).channel_id is None:
        err = discord.Embed(
          description = f"` Logs Channel ` of action ` {action} ` is already set to ` None `",
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
        description = f"Successfully set ` Logs Channel ` of action ` {action} ` to : ` None `",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      config.logs.clear(action)
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      embed = discord.Embed(
        description = f"Successfully set ` Logs Channel ` of action ` {action} ` to : {channel.mention}",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      config.logs.update(action, channel)
      await response.send_message(
        embed = embed,
        ephemeral = True
      )

  @configChannelWelcome.error
  @configChannelFarewell.error
  @configChannelLogs.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(GuildConfig(bot))