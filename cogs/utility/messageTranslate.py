import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands
from googletrans import Translator, constants

class MessageTranslate(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.tree.add_command(
      app_commands.ContextMenu(
        name = "Translate",
        callback = self.messageTranslate
      )
    )
    print("Loaded context menu : Translate")
    print("Loaded command : /translate")

  async def messageTranslate(self, interaction : discord.Interaction, message : discord.Message):
    response = interaction.response
    author = message.author
    translator = Translator()
    if (translator.translate(message.content, src = translator.detect(message.content).lang)).text.lower() == message.content.lower():
      err = discord.Embed(
        description = "This message is already in English language ! Cannot translate it any further",
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
    translation = translator.translate(message.content)
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_author(
      name = author.display_name,
      icon_url = author.display_avatar
    ).add_field(
      name = f"Original Message : ` {translation.src} `",
      value = translation.origin,
      inline = False
    ).add_field(
      name = f"Translation : ` {translation.dest} `",
      value = translation.text,
      inline = False
    )
    await response.send_message(
      embed = embed
    )

  async def langAutocomplete(self, interaction : discord.Interaction, current : str):
    return [
      app_commands.Choice(
        name = constants.LANGUAGES[langCode],
        value = langCode
      )
      for langCode in constants.LANGUAGES if current.lower() in constants.LANGUAGES[langCode].lower() or current.lower() in langCode.lower()
    ]

  @app_commands.command(
    name = "translate",
    description = "Translate a text"
  )
  @app_commands.describe(
    text = "The text to translate",
    src = "Origin language of text [ defaults to English ]",
    dest = "Language to translate the text to [ defaults to Engligh ]"
  )
  @app_commands.autocomplete(
    src = langAutocomplete,
    dest = langAutocomplete
  )
  async def translate(self, interaction : discord.Interaction, text : str, src : str = None, dest : str = "en"):
    response = interaction.response
    user = interaction.user
    translator = Translator()
    if src is None:
      src = translator.detect(text).lang
    elif src not in constants.LANGUAGES:
      err = discord.Embed(
        description = f"There is no such language as ` {dest} `",
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
    else:
      src = src
    if dest not in constants.LANGUAGES:
      err = discord.Embed(
        description = f"There is no such language as ` {dest} `",
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
    if src.lower() == "en" and dest.lower() == "en":
      err = discord.Embed(
        description = "Cannot translate from ` English ` to ` English `",
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
    translation = translator.translate(
      text,
      src = src,
      dest = dest
    )
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_author(
      name = user.display_name,
      icon_url = user.display_avatar
    ).add_field(
      name = f"Original Message : ` {translation.src} `",
      value = translation.origin,
      inline = False
    ).add_field(
      name = f"Translation : ` {translation.dest} `",
      value = translation.text,
      inline = False
    )
    await response.send_message(
      embed = embed
    )

  @translate.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(MessageTranslate(bot))