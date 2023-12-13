import discord
import nltk
import traceback
from discord import app_commands, ui
from nltk.corpus import wordnet
from discord.ext import commands

class Thesaurus(commands.GroupCog, name = "thesaurus", description = "Thesaurus commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /thesaurus synonym")
    print("Loaded command\t\t: /thesaurus antonym")

  @app_commands.command(
    name = "synonym",
    description = "Retrieve a synonym of a word"
  )
  @app_commands.describe(
    word = "Word to retrieve the synonym of"
  )
  async def thesaurusSynonym(self, interaction : discord.Interaction, word : str):
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

  @thesaurusSynonym.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

  @app_commands.command(
    name = "antonym",
    description = "Retrieve a antonym of a word"
  )
  @app_commands.describe(
    word = "Word to retrieve the antonym of"
  )
  async def thesaurusAntonym(self, interaction : discord.Interaction, word : str):
    response = interaction.response
    user = interaction.user
    await response.defer(
      ephemeral = True,
      thinking = True
    )
    antonymsList = []
    for antonym in wordnet.synsets(word):
      for l in antonym.lemmas():
        if l.antonyms():
          antonymsList.append(
            l.antonyms()[0].name()
          )
    if not antonymsList:
      err = discord.Embed(
        description = f"The word ` {word} ` does not have antonyms or is not a valid word",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await interaction.followup.send(
        embed = err
      )
      return
    wordSynonyms = ", ".join(list(set(antonymsList)))
    embed = discord.Embed(
      title = word.capitalize(),
      description = f"""
      **Antonyms** :
      > {wordSynonyms}
      """,
      color = 0x2b2d31
    )
    await interaction.followup.send(
      embed = embed
    )
  
  @thesaurusAntonym.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Thesaurus(bot))