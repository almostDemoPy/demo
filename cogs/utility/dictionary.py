import discord
import nltk
import traceback
from discord import app_commands, ui
from discord.ext import commands
from nltk.corpus import wordnet
from PyDictionary import PyDictionary

class DictionaryDefineViewSelect(ui.Select):
  def __init__(self, meanings, options):
    super().__init__(
      options = [
        discord.SelectOption(
          label = option
        )
        for option in options
      ],
      max_values = 1,
      min_values = 1,
      placeholder = "Select a Part of Speech :"
    )
    self.meanings = meanings

  async def callback(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    self.view.current = 0
    self.view.section = self.values[0]
    embedCopy = interaction.message.embeds[0].copy()
    embedCopy.description = f"""
    **{self.values[0].capitalize()}**
    > {self.meanings[self.values[0]][0]}
    """
    self.view.children[0].disabled = True
    if len(self.view.meanings[self.view.section]) == 1:
      self.view.children[1].disabled = True
    else:
      if self.view.children[1].disabled:
        self.view.children[1].disabled = False
    await response.edit_message(
      embed = embedCopy,
      view = self.view
    )

  async def on_error(self, interaction, error):
    traceback.print_exc()

class PreviousButton(ui.Button):
  def __init__(self):
    super().__init__(
      emoji = "◀",
      style = discord.ButtonStyle.primary,
      disabled = True
    )

  async def callback(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
      self.view.current -= 1
      if self.view.current == 0:
        self.disabled = True
      else:
        if self.disabled:
          self.disabled = False
      if self.view.children[1].disabled:
        self.view.children[1].disabled = False
      embed = interaction.message.embeds[0].copy()
      embed.description = f"""
      **{self.view.section}**
      > {self.view.meanings[self.view.section][self.view.current]}
      """
      await response.edit_message(
        embed = embed,
        view = self.view
      )
    except:
      traceback.print_exc()

class NextButton(ui.Button):
  def __init__(self):
    super().__init__(
      emoji = "▶",
      style = discord.ButtonStyle.primary
    )

  async def callback(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
      self.view.current += 1
      if self.view.current == len(self.view.meanings[self.view.section]) - 1:
        self.disabled = True
      else:
        if self.disabled:
          self.disabled = False
      if self.view.children[0].disabled:
        self.view.children[0].disabled = False
      embed = interaction.message.embeds[0].copy()
      embed.description = f"""
      **{self.view.section}**
      > {self.view.meanings[self.view.section][self.view.current]}
      """
      await response.edit_message(
        embed = embed,
        view = self.view
      )
    except:
      traceback.print_exc()

class DictionaryDefineView(ui.View):
  def __init__(self, meanings):
    super().__init__(
      timeout = None
    )
    self.meanings = meanings
    self.current = 0
    self.section = list(meanings.keys())[0]
    self.sectionList = list(meanings.keys())
    self.add_item(PreviousButton())
    self.add_item(NextButton())
    if len(self.meanings[self.section]) == 1:
      self.children[1].disabled = True
    if len(self.sectionList) > 1:
      self.add_item(DictionaryDefineViewSelect(meanings, self.sectionList))

  async def on_error(self, interaction, error):
    traceback.print_exc()

class Dictionary(commands.GroupCog, name = "dictionary", description = "dictionary commands"):
  def __init__(self, bot):
    self.bot = bot
    self.dictionary = PyDictionary()
    print("Loaded command : /dictionary define")

  @app_commands.command(
    name = "define",
    description = "Retrieve a definition of a word"
  )
  @app_commands.describe(
    word = "Word to define"
  )
  async def dictionaryDefine(self, interaction : discord.Interaction, word : str):
    response = interaction.response
    user = interaction.user
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    meanings = self.dictionary.meaning(word)
    if meanings is None:
      err = discord.Embed(
        description = f"` {word} ` is not a valid word",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await interaction.followup.send(
        embed = err
      )
    else:
      embed = discord.Embed(
        title = word.capitalize(),
        description = f"""
        **{list(meanings.keys())[0]}** :
        > {meanings[list(meanings.keys())[0]][0]}
        """,
        color = 0x2b2d31
      )
      await interaction.followup.send(
        embed = embed,
        view = DictionaryDefineView(meanings)
      )

  @dictionaryDefine.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

  @app_commands.command(
    name = "synonym",
    description = "Retrieve a synonym of a word"
  )
  @app_commands.describe(
    word = "Word to retrieve the synonym of"
  )
  async def dictionarySynonym(self, interaction : discord.Interaction, word : str):
    response = interaction.response
    user = interaction.user
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    synonymsList = []
    for synonym in wordnet.synsets(word):
      for l in synonym.lemmas():
        synonymsList.append(l.name())
    if not synonymsList:
      err = discord.Embed(
        description = f"The word ` {word} ` does not have synonyms or is not a valid word",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await interaction.followup.send(
        embed = err
      )
      return
    wordSynonyms = ", ".join(list(set(synonymsList)))
    embed = discord.Embed(
      title = word.capitalize(),
      description = f"""
      **Synonyms** :
      > {wordSynonyms}
      """,
      color = 0x2b2d31
    )
    await interaction.followup.send(
      embed = embed
    )

  @dictionarySynonym.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Dictionary(bot))