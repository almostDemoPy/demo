import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands

class SelectGame(ui.Select):
  def __init__(self, user, bot):
    super().__init__(
      placeholder = "Select an option :",
      options = [
        discord.SelectOption(
          label = "Chess"
        )
      ],
      max_values = 1,
      min_values = 1
    )
    self.user = user
    self.bot = bot

  async def callback(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      user = interaction.user
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
      selected = self.values[0]
      if selected == "Chess":
        embed = discord.Embed(
          title = "How to play Chess",
          description = f"""
            {self.bot.user.mention}'s Chess functions in algebraic notation. The type of algebraic notation the bot uses comes in two parts : the origin ( or selected ) tile / position of a piece, and the designated tile / position of the selected piece.

            **For example :**
            To move your pawn in tile ` e2 ` to tile ` e4 `, simply do ` e2e4 `. ` e2 ` is the origin tile / position of the pawn, while ` e4 ` is its designated tile.
          """,
          color = 0x2b2d31
        ).set_author(
          name = user.display_name,
          icon_url = user.display_avatar
        )
      await response.edit_message(
        embed = embed
      )
    except:
      traceback.print_exc()

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class HowTo(commands.GroupCog, name = "how", description = "How commands"):
  def __init__(self, bot):
    self.bot = bot

  howto = app_commands.Group(
    name = "to",
    description = "how to commands"
  )

  @howto.command(
    name = "play",
    description = "How to play a particular game"
  )
  async def howToPlay(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    view = ui.View().add_item(
      SelectGame(user, self.bot)
    )
    await response.send_message(
      view = view
    )

  @howToPlay.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await  bot.add_cog(HowTo(bot))