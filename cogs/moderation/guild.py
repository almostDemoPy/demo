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

class Guild(commands.GroupCog, name = "guild", description = "guild commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /guild emoji add")
    print("Loaded command\t\t: /guild emoji remove")
    print("Loaded command\t\t: /guild emoji info")

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
    newEmoji = await guild.create_custom_emoji(
      name = name,
      image = image
    )
    embed = discord.Embed(
      description = f"Successfully created a new emoji : {newEmoji.name} {newEmoji}"
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @emoji.command(
    name = "remove",
    description = "Remove an emoji from this guild"
  )
  @app_commands.describe(
    emoji = "Emoji to remove"
  )
  async def guildEmojiRemove(self, interaction : discord.Interaction, emoji : str):
    pass

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

  @app_commands.command(
    name = "edit",
    description = "Edit the current guild"
  )
  @app_commands.describe(
    name = "New name of the guild"
  )
  @app_commands.checks.cooldown(
    1, 300
  )
  async def guildEdit(self, interaction : discord.Interaction, name : str = None):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    if user != guild.owner:
      err = discord.Embed(
        description = "You do not have permission to modify this guild",
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
    if name is None:
      name = guild.name
    embed = discord.Embed(
      description = f"""
      Successfully edited the following :
      """,
      color = 0x2b2d31
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    if name is not None:
      embed.add_field(
        name = "Name :",
        value = f"> ` {name} `",
        inline = True
      )
    await guild.edit(
      name = name
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
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
  
  @guildEdit.error
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
      timeLeft = timedelta(
        seconds = int(error.retry_after)
      )
      err = discord.Embed(
        description = f"You can only modify the guild every ` 5 minutes `, try again <t:{int(timeLeft.total_seconds())}:R>",
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