import asyncio
import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class GuildConfig(commands.GroupCog, name = "config", description = "guild config commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /config channel welcome")
    print("Loaded command\t\t: /config channel farewell")
    print("Loaded command\t\t: /config channel logs")

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
      ),
      app_commands.Choice(
        name = "OnMessageDelete",
        value = "OnMessageDelete"
      ),
      app_commands.Choice(
        name = "OnMemberRemove",
        value = "OnMemberRemove"
      ),
      app_commands.Choice(
        name = "OnMemberUpdate",
        value = "OnMemberUpdate"
      ),
      app_commands.Choice(
        name = "OnMemberBan",
        value = "OnMemberBan"
      ),
      app_commands.Choice(
        name = "OnMemberUnban",
        value = "OnMemberUnban"
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

  _description = app_commands.Group(
    name = "description",
    description = "config description commands"
  )

  @_description.command(
    name = "welcome",
    description = "Configure this guild's welcomer description"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  async def configDescriptionWelcome(
    self,
    interaction : discord.Interaction
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
    embed = discord.Embed(
      description = """
      Please reply with the new welcomer description below :
      """,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).add_field(
      name = "Old Welcome Description :",
      value = f"{config.welcome.description}",
      inline = False
    ).add_field(
      name = "Syntaxes :",
      value = """
      ` {member.mention} ` : mention the member
      ` {guild.name} ` : get the current guild name
      """
    ).set_footer(
      text = "Timeout : 10 minutes"
    )
    await response.send_message(
      embed = embed
    )
    origRes = await interaction.original_response()
    msg = None
    while msg is None:
      def messageCheck(message):
        if message.reference is None:
          return False
        return message.author == user and message.channel == interaction.channel and message.reference.message_id == origRes.to_reference().message_id
      try:
        msg = await self.bot.wait_for(
          "message",
          check = messageCheck,
          timeout = 600
        )
      except asyncio.TimeoutError:
        err = discord.Embed(
          description = "Action Timed Out",
          color = 0xff3131
        ).set_author(
          name = self.bot.user.display_name,
          icon_url = self.bot.user.display_avatar
        )
        await interaction.edit_original_response(
          embed = err
        )
        return
    newDescription = msg.content
    config.welcome.set_description(newDescription)
    embed = discord.Embed(
      description = f"""
      Successfully set ` Welcome Description ` to :

      {newDescription}
      """,
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await interaction.edit_original_response(
      embed = embed
    )

  @_description.command(
    name = "farewell",
    description = "Configure this guild's farewell description"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  async def configDescriptionFarewell(
    self,
    interaction : discord.Interaction
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
    embed = discord.Embed(
      description = """
      Please reply with the new farewell description below :
      """,
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).add_field(
      name = "Old Farewell Description :",
      value = f"{config.farewell.description}",
      inline = False
    ).add_field(
      name = "Syntaxes :",
      value = """
      ` {member.mention} ` : mention the member
      ` {guild.name} ` : get the current guild name
      """
    ).set_footer(
      text = "Timeout : 10 minutes"
    )
    await response.send_message(
      embed = embed
    )
    origRes = await interaction.original_response()
    msg = None
    while msg is None:
      def messageCheck(message):
        if message.reference is None:
          return False
        return message.author == user and message.channel == interaction.channel and message.reference.message_id == origRes.to_reference().message_id
      try:
        msg = await self.bot.wait_for(
          "message",
          check = messageCheck,
          timeout = 600
        )
      except asyncio.TimeoutError:
        err = discord.Embed(
          description = "Action Timed Out",
          color = 0xff3131
        ).set_author(
          name = self.bot.user.display_name,
          icon_url = self.bot.user.display_avatar
        )
        await interaction.edit_original_response(
          embed = err
        )
        return
    newDescription = msg.content
    config.farewell.set_description(newDescription)
    embed = discord.Embed(
      description = f"""
      Successfully set ` Welcome Description ` to :

      {newDescription}
      """,
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await interaction.edit_original_response(
      embed = embed
    )

  @configChannelWelcome.error
  @configChannelFarewell.error
  @configChannelLogs.error
  @configDescriptionWelcome.error
  @configDescriptionFarewell.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(GuildConfig(bot))