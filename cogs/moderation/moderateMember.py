import discord
import traceback
from datetime import datetime, timedelta
from discord import app_commands, ui
from discord.ext import commands

class TimeoutModal(ui.Modal):
  def __init__(self, member, user, bot):
    super().__init__(
      timeout = None,
      title = "Moderate > Timeout"
    )
    self.member = member
    self.user = user
    self.bot = bot

  seconds = ui.TextInput(
    label = "seconds : 0 - 2419200",
    default = "60",
    required = True,
    max_length = 7,
    min_length = 1
  )

  minutes = ui.TextInput(
    label = "minutes : 0 - 40320",
    default = "0",
    required = True,
    max_length = 5,
    min_length = 1
  )

  hours = ui.TextInput(
    label = "hours : 0 - 672",
    default = "0",
    required = True,
    max_length = 3,
    min_length = 1
  )

  days = ui.TextInput(
    label = "days : 0 - 28",
    default = "0",
    required = True,
    max_length = 2,
    min_length = 1
  )

  reason = ui.TextInput(
    label = "reason :",
    default = "",
    required = False,
    max_length = 512
  )

  async def on_submit(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
      try:
        seconds = int(str(self.seconds))
        if seconds < 0 or seconds > 2_419_200:
          err = discord.Embed(
            description = "` seconds ` must only be between ` 0 ` and ` 2419200 `",
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
      except:
        err = discord.Embed(
          description = "` seconds ` must take an input of ` int `",
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
      try:
        minutes = int(str(self.minutes))
        if minutes < 0 or minutes > 40320:
          err = discord.Embed(
            description = "` minutes ` must be only between ` 0 ` and ` 40320 `",
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
      except:
        err = discord.Embed(
          description = "` minutes ` must take an input of ` int `",
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
      try:
        hours = int(str(self.hours))
        if hours < 0 or hours > 672:
          err = discord.Embed(
            description = "` hours ` must be only between ` 0 ` and ` 672 `",
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
      except:
        err = discord.Embed(
          description = "` hours ` must take an input of ` int `",
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
      try:
        days = int(str(self.days))
        if days < 0 or days > 28:
          err = discord.Embed(
            description = "` days ` must be only between ` 0 ` and ` 28 `",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = selef.bot.user.display_avatar
          )
          await response.send_message(
            embe = err,
            ephemeral = True
          )
          return
      except:
        err = discord.Embed(
          description = "` days ` must take an input of ` int `",
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
      reason = None if str(self.reason) == "" else str(self.reason)
      duration = timedelta(
        seconds = seconds,
        minutes = minutes,
        hours = hours,
        days = days
      )
      if duration.days > 28:
        err = discord.Embed(
          description = "You can only timeout a member for 28 days maximum",
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
      timedOutUntil = datetime.today() + duration
      embed = discord.Embed(
        description = f"Successfully timed out {self.member.mention}. The time out expires <t:{int(timedOutUntil.timestamp())}:R>",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      if reason is not None:
        embed.add_field(
          name = "Reason :",
          value = reason
        )
      await self.member.timeout(
        duration,
        reason = reason
      )
      await response.edit_message(
        embed = embed,
        view = None
      )
    except:
      traceback.print_exc()

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class KickModal(ui.Modal):
  def __init__(self, member, user, bot):
    super().__init__(
      timeout = None,
      title = "Moderate > Kick"
    )
    self.member = member
    self.user = user
    self.bot = bot

  reason = ui.TextInput(
    label = "reason :",
    default = "",
    required = False
  )

  async def on_submit(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    reason = str(self.reason) if str(reason) != "" else None
    embed = discord.Embed(
      description = f"Successfully kicked {member.mention} !",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    if reason is not None:
      embed.add_field(
        name = "Reason :",
        value = reason
      )
    await self.member.kick(
      reason = reason
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class BanModal(ui.Modal):
  def __init___(self, member, user, bot):
    super().__init__(
      title = "Moderate > Ban"
    )
    self.member = member
    self.user = user
    self.bot = bot

  reason = ui.TextInput(
    label = "reason :",
    default = "",
    required = False
  )

  async def on_submit(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    reason = None if str(self.reason) == "" else str(self.reason)
    embed = discord.Embed(
      description = f"Successfully banned {self.member.mention}",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await self.member.ban(
      reason = reason
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class ActionSelect(ui.Select):
  def __init__(self, member, user, bot):
    super().__init__(
      placeholder = "Select an action :",
      max_values = 1,
      min_values = 1,
      options = [
        discord.SelectOption(
          label = "Ban"
        ),
        discord.SelectOption(
          label = "Kick"
        ),
        discord.SelectOption(
          label = "Timeout"
        )
      ]
    )
    self.member = member
    self.user = user
    self.bot = bot

  async def callback(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
      guild = interaction.guild
      guildUser = guild.get_member(user.id)
      guildBot = guild.get_member(self.bot.user.id)
      if user != self.user:
        err = discord.Embed(
          description = "This is not your menu !",
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
      action = self.values[0]
      if action == "Timeout":
        if not guildUser.guild_permissions.moderate_members:
          err = discord.Embed(
            description = f"You do not have permission to timeout {self.member.mention}",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await response.edit_message(
            embed = err
          )
          return
        if not guildBot.guild_permissions.moderate_members:
          err = discord.Embed(
            description = f"I do not have permission to timeout {self.member.mention}",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await response.edit_message(
            embed = err
          )
          return
        await response.send_modal(
          TimeoutModal(self.member, self.user, self.bot)
        )
      elif action == "Kick":
        if not guildUser.guild_permissions.kick_members:
          err = discord.Embed(
            description = f"You do not have permission to kick {self.member.mention}",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await response.edit_message(
            embed = err
          )
          return
        if not guildBot.guild_permissions.kick_members:
          err = discord.Embed(
            description = f"I do not have permission to kick {self.member.mention}",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await response.edit_message(
            embed = err
          )
          return
        await response.send_modal(
          KickModal(self.member, self.user, self.bot)
        )
      elif action == "Ban":
        if not guildUser.guild_permissions.ban_members:
          err = discord.Embed(
            description = f"You do not have permission to ban {self.member.mention}",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await response.edit_message(
            embed = err
          )
          return
        if not guildBot.guild_permissions.ban_members:
          err = discord.Embed(
            description = f"I do not have permission to ban {self.member.mention}",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await response.edit_message(
            embed = err
          )
          return
        await response.send_modal(
          BanModal(self.member, self.user, self.bot)
        )
    except:
      traceback.print_exc()

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class ModerateMember(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.moderateContextMenu = app_commands.ContextMenu(
      name = "Moderate",
      callback = self.selectAction
    )
    self.bot.tree.add_command(
      self.moderateContextMenu
    )
    print("Loaded context menu\t: moderate")
    print("Loaded command\t\t: /moderate timeout")
    print("Loaded command\t\t: /moderate kick")
    print("Loaded command\t\t: /moderate ban")
    print("Loaded command\t\t: /moderate unban")
    print("Loaded command\t\t: /moderate cleanup")

  moderate = app_commands.Group(
    name = "moderate",
    description = "Moderate commands"
  )
  
  async def selectAction(self, interaction : discord.Interaction, member : discord.Member):
    try:
      response = interaction.response
      user = interaction.user
      if member == interaction.guild.owner:
        err = discord.Embed(
          description = "Unable to moderate the **Guild Owner**",
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
      if member.bot:
        err = discord.Embed(
          description = "Unable to moderate a **Discord bot**",
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
      if member == self.bot.user:
        err = discord.Embed(
          description = "Unable to moderate myself",
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
        description = f"Select an action to take on for {member.mention} :",
        color = 0x2b2d31
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      view = ui.View().add_item(
        ActionSelect(member, user, self.bot)
      )
      await response.send_message(
        embed = embed,
        view = view,
        ephemeral = True
      )
    except:
      traceback.print_exc()
    
  @moderate.command(
    name = "timeout",
    description = "Timeout a member"
  )
  @app_commands.checks.has_permissions(
    moderate_members = True
  )
  @app_commands.describe(
    member = "Select a member to timeout :",
    seconds = "0 - 2419200 seconds ( Defaults to 60 seconds )",
    minutes = "0 - 40320 minutes ( Defaults to 0 minutes )",
    hours = "0 - 672 hours ( Defaults to 0 hours )",
    days = "0 - 28 days ( Defaults to 0 days )",
    reason = "Reason to timeout the member"
  )
  async def moderateTimeout(self, interaction : discord.Interaction, member : discord.Member, seconds : app_commands.Range[int, 0, 2419200] = 60, minutes : app_commands.Range[int, 0, 40320] = 0, hours : app_commands.Range[int, 0, 672] = 0, days : app_commands.Range[int, 0, 28] = 0, reason : str = None):
    response = interaction.response
    user = interaction.user
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "Unable to timeout the **Guild Owner**",
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
    if member.bot:
      err = discord.Embed(
        description = "Unable to timeout a **Discord bot**",
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
    if member == self.bot.user:
      err = discord.Embed(
        description = "Unable to timeout myself",
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
    if seconds < 0 or seconds > 2_419_200:
      err = discord.Embed(
        description = "` seconds ` must only be between ` 0 ` and ` 2419200 `",
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
    elif minutes < 0 or minutes > 40320:
      err = discord.Embed(
        description = "` minutes ` must only be between ` 0 ` and ` 40320 `",
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
    elif hours < 0 or hours > 672:
      err = discord.Embed(
        description = "` hours ` must only be between ` 0 ` and ` 672 `",
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
    elif days < 0 or days > 28:
      err = discord.Embed(
        description = "` days ` must only be between ` 0 ` and ` 28 `",
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    duration = timedelta(
      seconds = seconds,
      minutes = minutes,
      hours = hours,
      days = days
    )
    if int(duration.total_seconds()) == 0:
      embed = discord.Embed(
        description = f"Successfully removed {member.mention}'s timeout",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await member.timeout(
        None,
        reason = reason
      )
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      if duration.days > 28:
        err = discord.Embed(
          description = "You can only timeout a member for 28 days maximum",
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
      expires = datetime.today() + duration
      embed = discord.Embed(
        description = f"Successfully timed out {member.mention}. The timeout will expire <t:{int(expires.timestamp())}:R>",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await member.timeout(
        duration,
        reason = reason
      )
      await response.send_message(
        embed = embed,
        ephemeral = True
      )

  @moderateTimeout.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    if isinstance(error, app_commands.MissingPermissions):
      err = discord.Embed(
        description = "You do not have the permission to timeout a member",
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
    elif isinstance(error, app_commands.BotMissingPermissions):
      err = discord.Embed(
        description = "I do not have the permission to timeout a member",
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

  @moderate.command(
    name = "kick",
    description = "Kick a member"
  )
  @app_commands.describe(
    member = "Select a member to kick :",
    reason = "Reason to kick the member"
  )
  @app_commands.checks.has_permissions(
    kick_members = True
  )
  async def moderateKick(self, interaction : discord.Interaction, member : discord.Member, reason : str = None):
    response = interaction.response
    user = interaction.user
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "Unable to kick the **Guild Owner**",
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
    if member == self.bot.user:
      err = discord.Embed(
        description = "Unable to kick myself",
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
    await response.defer(
      thinking = True,
      ephemeral = True
    )
    if user != interaction.guild.owner:
      userRoles = user.roles.reverse()
      memberRoles = member.roles.reverse()
      userKickRole = None
      memberKickRole = None
      for role in userRoles:
        if role.permissions.kick_members or role.permissions.administrator:
          userKickRole = role
          break
      for role in memberRoles:
        if role.permissions.kick_members or role.permissions.administrator:
          memberKickRole = role
          break
      if userKickRole is not None and memberKickRole is not None:
        if memberKickRole >= userKickRole:
          err = discord.Embed(
            description = "You cannot kick someone higher than or as equal as you",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await interaction.followup.send(
            embed = err
          )
          return
    embed = discord.Embed(
      description = f"Successfully kicked {member.mention}",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    if reason is not None:
      embed.add_field(
        name = "Reason :",
        value = reason
      )
    await member.kick(
      reason = reason
    )
    await interaction.followup.send(
      embed = embed
    )

  @moderateKick.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    if isinstance(error, app_commands.MissingPermissions):
      err = discord.Embed(
        description = "You do not have permission to kick a member",
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
    elif isinstance(error, app_commands.MissingPermissions):
      err = discord.Embed(
        description = "I do not have permission to kick a member",
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

  @moderate.command(
    name = "ban",
    description = "Ban a member"
  )
  @app_commands.describe(
    member = "Select a member to ban :",
    reason = "Reason to ban the member"
  )
  @app_commands.checks.has_permissions(
    ban_members = True
  )
  async def moderateBan(self, interaction : discord.Interaction, member : discord.Member, reason : str = None):
    response = interaction.response
    user = interaction.user
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "Unable to ban a **Guild Owner**",
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
    if member == self.bot.user:
      err = discord.Embed(
        description = "Unable to ban myself",
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
    await response.defer(
      thinking = True,
      ephemeral = True
    )
    if user != interaction.guild.owner:
      userRoles = user.roles.reverse()
      memberRoles = member.roles.reverse()
      userBanRole = None
      memberBanRole = None
      for role in userRoles:
        if role.permissions.ban_members or role.permissions.administrator:
          userBanRole = role
          break
      for role in memberRoles:
        if role.permissions.ban_members or role.permissions.administrator:
          memberBanRole = role
          break
      if userBanRole is not None and memberBanRole is not None:
        if memberBanRole >= userBanRole:
          err = discord.Embed(
            description = "You cannot ban someone higher than or as equal as you",
            color = 0xff3131
          ).set_author(
            name = self.bot.user.display_name,
            icon_url = self.bot.user.display_avatar
          )
          await interaction.followup.send(
            embed = err
          )
          return
    embed = discord.Embed(
      description = f"Successfully banned {member.mention}",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await member.ban(
      reason = reason
    )
    await interaction.followup.send(
      embed = embed
    )

  @moderateBan.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    if isinstance(error, app_commands.MissingPermissions):
      err = discord.Embed(
        description = "You do not have permission to ban a member",
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
    elif isinstance(error, app_commands.BotMissingPermissions):
      err = discord.Embed(
        description = "I do not have permission to ban a member",
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

  @moderate.command(
    name = "unban",
    description = "Unban a member"
  )
  @app_commands.describe(
    member = "Select a member to unban :",
    reason = "Reason to unban the member"
  )
  @app_commands.checks.has_permissions(
    ban_members = True
  )
  async def moderateUnban(self, interaction : discord.Interaction, member : discord.Member, reason : str = None):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if member == guild.owner:
      err = discord.Embed(
        description = "Unable to unban a **Guild Owner**",
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
    if member == self.bot.user:
      err = discord.Embed(
        descripition = "Unable to unban myself",
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
    if member not in [banned async for banned in guild.bans()]:
      err = discord.Embed(
        description = f"{member.mention} is not banned",
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
      description = f"Successfully unbanned {member.mention}",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    if reason is not None:
      embed.add_field(
        name = "Reason :",
        value = reason
      )
    await member.unban(reason = reason)
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @moderateUnban.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    if isinstance(error, app_commands.MissingPermissions):
      err = discord.Embed(
        description = "You do not have permission to unban a member",
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
    elif isinstance(error, app_commands.BotMissingPermissions):
      err = discord.Embed(
        description = "I do not have permission to unban a member",
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

  @moderate.command(
    name = "cleanup",
    description = "Clean up the current channel"
  )
  @app_commands.describe(
    limit = "amount of messages to delete",
    member = "member's messages to delete",
    reason = "reason to delete messages"
  )
  @app_commands.checks.has_permissions(
    manage_messages = True
  )
  async def moderateCleanUp(self, interaction : discord.Interaction, limit : app_commands.Range[int, 1, 100], member : discord.Member = None, reason : str = None):
    response = interaction.response
    user = interaction.user
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    def messageCheck(message):
      if member is None:
        return True
      return message.author == member
    deleted = await interaction.channel.purge(
      limit = limit,
      check = messageCheck,
      reason = reason
    )
    embed = discord.Embed(
      description = f"Successfully deleted {len(deleted):,} messages in this channel",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await interaction.followup.send(
      embed = embed
    )

  @moderateCleanUp.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    if isinstance(error, app_commands.MissingPermissions):
      err = discord.Embed(
        description = "You do not have permission to clean up the channel",
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
    if isinstance(error, app_commands.BotMissingPermissions):
      err = discord.Embed(
        description = "I do not have permission to clean up the channel",
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

async def setup(bot):
  await bot.add_cog(ModerateMember(bot))