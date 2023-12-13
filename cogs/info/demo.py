import discord
import traceback
from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands

class Demo(commands.GroupCog, name = "demo", description = "demo commands"):
  def __init__(self, bot):
    self.bot = bot
    self.startup = datetime.now()
    print("Loaded command\t\t: /demo info")

  @app_commands.command(
    name = "info",
    description = "Demo's info"
  )
  async def demoInfo(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    botMember = guild.me
    owner = guild.get_member(self.bot.owner_id)
    if owner is not None:
      botOwner = owner.mention
    else:
      botOwner = "` demoutrei `"
    embed = discord.Embed(
      title = self.bot.user.display_name,
      description = f"""
      **Developer** : {botOwner}
      **Developer ID** : ||` 1057104290600189972 `||
      **User ID** : ||` {self.bot.user.id} `||
      **Created** : <t:{int(self.bot.user.created_at.timestamp())}:R>
      **Joined** : <t:{int(botMember.joined_at.timestamp())}:R>
      """,
      color = 0x2b2d31
    ).set_thumbnail(
      url = self.bot.user.display_avatar
    ).add_field(
      name = "Command Prefix :",
      value = "> ` demo.<command_name> `",
      inline = True
    ).add_field(
      name = "Guild Count :",
      value = f"> {len(self.bot.guilds):,}",
      inline = True
    ).add_field(
      name = "User Count :",
      value = f"> {len(self.bot.users):,}",
      inline = True
    ).add_field(
      name = "Online Since :",
      value = f"> <t:{int(self.startup.timestamp())}:R>",
      inline = True
    )
    view = ui.View().add_item(
      ui.Button(
        label = "Support Server",
        url = "https://discord.gg/mXSXzc4SJB"
      )
    )
    await response.send_message(
      embed = embed,
      view = view
    )

  @demoInfo.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Demo(bot))