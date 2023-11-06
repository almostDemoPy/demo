import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands

class PollSelect(ui.Select):
  def __init__(self, embedFieldNamesList):
    super().__init__(
      min_values = 1,
      max_values = 1,
      placeholder = "Select a choice :"
    )
    self.choices = {}
    for fieldName in embedFieldNamesList:
      self.choices[fieldName] = []
    self.options = [
      discord.SelectOption(
        label = fieldName
      )
      for fieldName in self.choices.keys()
    ]
    self.embedFieldNamesList = embedFieldNamesList

  async def callback(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
      selected = self.values[0]
      if user.id in self.choices[selected]:
        self.choices[selected].remove(user.id)
      else:
        originalSelection = None
        for choice in self.choices:
          if user.id in self.choices[choice]:
            originalSelection = choice
            break
          else:
            continue
        if originalSelection is not None:
          self.choices[originalSelection].remove(user.id)
        self.choices[selected].append(user.id)
      totalVotes = 0
      embed = interaction.message.embeds[0].copy().clear_fields()
      for choice in self.choices:
        totalVotes += len(self.choices[choice])
      for choice in self.choices:
        voteCount = len(self.choices[choice])
        if voteCount == 0:
          votePercent = 0
        else:
          votePercent = (voteCount / totalVotes) * 100
        embed.add_field(
          name = choice,
          value = f"> Voted : ` {voteCount:,} ` | ` {votePercent:.2f} % `",
          inline = False
        )
      await response.edit_message(
        embed = embed
      )
    except:
      traceback.print_exc()

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class PollView(ui.View,):
  def __init__(self):
    super().__init__(
      timeout = None
    )

  async def on_error(self, interaction : discord.Interaction):
    traceback.print_exc()

class PollModal(ui.Modal):
  def __init__(self, question):
    super().__init__(
      timeout = None,
      title = question
    )
    self.question = question

  choice_1 = ui.TextInput(
    label = "Choice 1 :",
    default = "",
    max_length = 100,
    style = discord.TextStyle.short,
    required = True
  )

  choice_2 = ui.TextInput(
    label = "Choice 2 :",
    default = "",
    max_length = 100,
    style = discord.TextStyle.short,
    required = True
  )

  choice_3 = ui.TextInput(
    label = "Choice 3 :",
    default = "",
    max_length = 100,
    style = discord.TextStyle.short,
    required = False
  )

  choice_4 = ui.TextInput(
    label = "Choice 4 :",
    default = "",
    max_length = 100,
    style = discord.TextStyle.short,
    required = False
  )

  choice_5 = ui.TextInput(
    label = "Choice 5 :",
    default = "",
    max_length = 100,
    style = discord.TextStyle.short,
    required = False
  )

  async def on_submit(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
      optionsList = []
      embed = discord.Embed(
        description = f"""
**Question** :
{self.question}
        """,
        color = 0x2b2d31
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      for choice in [self.choice_1, self.choice_2, self.choice_3, self.choice_4, self.choice_5]:
        if choice.value != "":
          optionsList.append(
            discord.SelectOption(
              label = choice.value
            )
          )
          embed.add_field(
            name = choice.value,
            value = f"> Voted : ` 0 ` | ` 0.00 % `",
            inline = False
          )
      embedFieldNamesList = [field.name for field in embed.fields]
      view = ui.View().add_item(
        PollSelect(embedFieldNamesList)
      )
      await response.send_message(
        embed = embed,
        view = view
      )
    except:
      traceback.print_exc()

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class Polls(commands.GroupCog, name = "poll", description = "Poll commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command group : poll")

  @app_commands.command(
    name = "create",
    description = "Create a poll"
  )
  @app_commands.describe(
    question = "Question to ask"
  )
  async def pollCreate(self, interaction : discord.Interaction, question : str):
    response = interaction.response
    user = interaction.user
    await response.send_modal(PollModal(question))

  @pollCreate.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Polls(bot))