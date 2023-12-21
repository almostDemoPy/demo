import discord
import traceback
from datetime import datetime, timedelta
from discord import app_commands, ui
from discord.ext import commands

class GuildEmojiInfoSelect(ui.Select):
  def __init__(self, emojis):
    super().__init__(
      placeholder = "Select an emoji :",
      options = [
        discord.SelectOption(
          label = emoji.name,
          value = emoji.id,
          emoji = emoji
        )
        for emoji in emojis
      ],
      min_values = 1,
      max_values = 1
    )

  async def callback(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    emoji = await guild.fetch_emoji(self.values[0])
    embed = discord.Embed(
      title = emoji.name,
      description = f"""
      **Emoji ID** : ` {emoji.id} `
      **Created** : <t:{int(emoji.created_at.timestamp())}:R>
      """,
      color = 0x2b2d31
    ).set_thumbnail(
      url = emoji.url
    ).add_field(
      name = "Is Animated ?",
      value = f"> ` {emoji.animated} `",
      inline = True
    )
    if emoji.user is not None:
      embed.add_field(
        name = "Creator :",
        value = f"> {emoji.user.mention}",
        inline = True
      )
    await response.edit_message(
      embed = embed
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class GuildEmojiRemoveSelect(ui.Select):
  def __init__(self, emojis):
    super().__init__(
      placeholder = "Select an emoji :",
      options = [
        discord.SelectOption(
          label = emoji.name,
          value = emoji.id,
          emoji = emoji
        )
        for emoji in emojis
      ],
      min_values = 1,
      max_values = 1
    )

  async def callback(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    emoji = guild.get_emoji(self.values[0])
    await emoji.delete()
    embed = discord.Embed(
      description = f"Successfully deleted emoji with name : ` {emoji.name} `",
      color = 0x39ff14
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class GuildEditDescriptionModal(ui.Modal):
  def __init__(self, guild : discord.Guild, bot):
    super().__init__(
      title = "Guild Edit Description"
    )
    self.guild = guild
    self.bot = bot
    if guild.description is None:
      self.defaultDescription = ""
    else:
      self.defaultDescription = guild.description
    self.descriptionField = ui.TextInput(
      label = "Guild Description :",
      default = self.defaultDescription,
      max_length = 120,
      min_length = 0,
      required = False,
      placeholder = "Leave empty to remove the description",
      style = discord.TextStyle.long
    )
    self.add_item(self.descriptionField)

  async def on_submit(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    newDescription = str(self.descriptionField)
    if newDescription == "":
      newDescription = None
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    followup = interaction.followup
    oldDescription = guild.description
    embed = discord.Embed(
      description = f"Successfully edited the guild property : ` description `",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    ).add_field(
      name = "Old :",
      value = f">>> {guild.description}",
      inline = False
    ).add_field(
      name = "New :",
      value = f">>> {newDescription}",
      inline = False
    )
    await guild.edit(
      description = newDescription
    )
    await followup.send(
      embed = embed
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class Guild(commands.GroupCog, name = "guild", description = "guild commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /guild emoji add")
    print("Loaded command\t\t: /guild emoji remove")
    print("Loaded command\t\t: /guild emoji info")
    print("Loaded command\t\t: /guild edit name")
    print("Loaded command\t\t: /guild edit description")
    print("Loaded command\t\t: /guild edit icon")

  emoji = app_commands.Group(
    name = "emoji",
    description = "guild emoji commands"
  )

  @emoji.command(
    name = "add",
    description = "Add an emoji to this guild"
  )
  @app_commands.describe(
    name = "Name of the emoji",
    image = "Image of the emoji"
  )
  async def guildEmojiAdd(self, interaction : discord.Interaction, name : str, image : discord.Attachment):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != guild.owner:
      err = discord.Embed(
        description = "Only the Guild Owner can execute this slash command",
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
    if len(guild.emojis) == guild.emoji_limit:
      err = discord.Embed(
        description = "This server does not have any empty emoji slots left",
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
    emojiBytes = await image.read()
    newEmoji = await guild.create_custom_emoji(
      name = name,
      image = emojiBytes
    )
    embed = discord.Embed(
      description = f"Successfully created a new emoji : {newEmoji.name} {newEmoji}",
      color = 0x39ff14
    )
    await interaction.followup.send(
      embed = embed
    )

  @emoji.command(
    name = "remove",
    description = "Remove an emoji from this guild"
  )
  @app_commands.describe(
    name = "Name of emoji to remove"
  )
  async def guildEmojiRemove(self, interaction : discord.Interaction, name : str):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != guild.owner:
      err = discord.Embed(
        description = "Only the Guild Owner can execute this slash command",
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
    selectedEmojiList = [emoji for emoji in guild.emojis if emoji.name == name]
    if not selectedEmojiList:
      err = discord.Embed(
        description = f"There is no emoji in this guild with name ` {name} `",
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
    if len(selectedEmojiList) == 1:
      await guild.delete_emoji(selectedEmojiList[0])
      embed = discord.Embed(
        description = f"Successfully deleted emoji with name : ` {name} `",
        color = 0x39ff14
      )
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      if len(selectedEmojiList) > 25:
        selectedEmojiList = selectedEmojiList[:25]
      view = ui.View().add_item(
        GuildEmojiRemoveSelect(selectedEmojiList)
      )
      embed = discord.Embed(
        description = "Select an emoji below :",
        color = 0x2b2d31
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await response.send_message(
        embed = embed,
        view = view,
        ephemeral = True
      )

  @emoji.command(
    name = "info",
    description = "Retrieve the info of an emoji"
  )
  @app_commands.describe(
    name = "Name of an emoji to retrieve"
  )
  async def guildEmojiInfo(self, interaction : discord.Interaction, name : str):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    selectedEmojiList = [emoji for emoji in guild.emojis if emoji.name == name]
    if not selectedEmojiList:
      err = discord.Embed(
        description = f"There is no emoji in this guild with name ` {name} `",
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
    if len(selectedEmojiList) == 1:
      emoji = await guild.fetch_emoji(selectedEmojiList[0].id)
      embed = discord.Embed(
        title = emoji.name,
        description = f"""
        **Emoji ID** : ` {emoji.id} `
        **Created** : <t:{int(emoji.created_at.timestamp())}:R>
        """,
        color = 0x2b2d31
      ).set_thumbnail(
        url = emoji.url
      ).add_field(
        name = "Is Animated ?",
        value = f"> ` {emoji.animated} `",
        inline = True
      )
      if emoji.user is not None:
        embed.add_field(
          name = "Creator :",
          value = f"> {emoji.user.mention}",
          inline = True
        )
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
    else:
      if len(selectedEmojiList) > 25:
        selectedEmojiList = selectedEmojiList[:25]
      view = ui.View().add_item(
        GuildEmojiInfoSelect(selectedEmojiList)
      )
      embed = discord.Embed(
        description = "Select an emoji below :",
        color = 0x2b2d31
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await response.send_message(
        embed = embed,
        view = view,
        ephemeral = True
      )

  edit = app_commands.Group(
    name = "edit",
    description = "guild edit commands"
  )

  @edit.command(
    name = "name",
    description = "Change the current guild's name"
  )
  @app_commands.describe(
    name = "New guild name :"
  )
  @app_commands.checks.cooldown(
    1, 300
  )
  @app_commands.default_permissions(
    administrator = True
  )
  async def guildEditName(
    self,
    interaction : discord.Interaction,
    name : app_commands.Range[str, 2, 100]
  ):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != interaction.guild.owner:
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
    await response.defer(
      thinking = True,
      ephemeral = True
    )
    followup = interaction.followup
    before = guild.name
    await guild.edit(
      name = name
    )
    embed = discord.Embed(
      description = "Successfully edited the guild property : ` name `",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    ).add_field(
      name = "Old :",
      value = f"> {before}",
      inline = True
    ).add_field(
      name = "New :",
      value = f"> {name}",
      inline = True
    )
    await followup.send(
      embed = embed
    )

  @edit.command(
    name = "description",
    description = "Change the current guild's description"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  async def guildEditDescription(
    self,
    interaction : discord.Interaction
  ):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != interaction.guild.owner:
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
    if "COMMUNITY" not in guild.features:
      err = discord.Embed(
        description = "` Community ` is not enabled in this server",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await followup.send(
        embed = err
      )
      return
    await response.send_modal(
      GuildEditDescriptionModal(guild, self.bot)
    )

  @edit.command(
    name = "icon",
    description = "Change the current guild's icon"
  )
  @app_commands.describe(
    image = "New icon :"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  @app_commands.checks.cooldown(
    1, 300
  )
  async def guildEditIcon(
    self,
    interaction : discord.Interaction,
    image : discord.Attachment = None
  ):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != interaction.guild.owner:
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
    if image is not None:
      if not (image.filename.endswith(".png") or image.filename.endswith(".jpeg") or image.filename.endswith(".gif")):
        err = discord.Embed(
          description = "only ` .PNG `, ` .JPEG `, or ` .GIF ` is supported",
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
      if image.filename.endswith(".png") or image.filename.endswith(".jpeg"):
        image = await image.read()
      else:
        if "ANIMATED_ICON" not in guild.features:
          err = discord.Embed(
            description = "This server does not support animated icons yet",
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
        image = await image.read()
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    followup = interaction.followup
    await guild.edit(
      icon = image
    )
    embed = discord.Embed(
      description = "Successfully edited guild property : ` icon `",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await followup.send(
      embed = embed
    )

  @app_commands.command(
    name = "banner",
    description = "Change the current guild's banner"
  )
  @app_commands.describe(
    image = "New banner :"
  )
  @app_commands.default_permissions(
    administrator = True
  )
  @app_commands.checks.cooldown(
    1, 300
  )
  async def guildEditBanner(
    self,
    interaction : discord.Interaction,
    image : discord.Attachment = None
  ):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != interaction.guild.owner:
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
    if "BANNER" not in guild.features:
      err = discord.Embed(
        description = "This server does not support guild banners yet",
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
    if image is not None:
      image = await image.read()
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    followup = interaction.followup
    await guild.edit(
      banner = image
    )
    embed = discord.Embed(
      description = "Successfully edited guild property : ` banner `",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await followup.send(
      embed = embed
    )

  @guildEmojiAdd.error
  @guildEmojiRemove.error
  async def error(self, interaction : discord.Interaction, error):
    response = interaction.response
    traceback.print_exc()
    if isinstance(error, app_commands.BotMissingPermissions):
      err = discord.Embed(
        description = "I do not have permissions to create / remove emojis in this server",
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

  @guildEmojiInfo.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
  
  @guildEditName.error
  @guildEditDescription.error
  @guildEditIcon.error
  @guildEditBanner.error
  async def error(self, interaction : discord.Interaction, error):
    response = interaction.response
    traceback.print_exc()
    if isinstance(error, app_commands.BotMissingPermissions):
      err = discord.Embed(
        description = "I do not have permissions to modify this guild",
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
    elif isinstance(error, app_commands.CommandOnCooldown):
      timeDiff = timedelta(
        seconds = int(error.retry_after)
      )
      timeLeft = datetime.now() + timeDiff
      err = discord.Embed(
        description = f"You can only modify the guild every ` 5 minutes `, try again <t:{int(timeLeft.timestamp())}:R>",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )

async def setup(bot):
  await bot.add_cog(Guild(bot))