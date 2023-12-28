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
    print("Loaded command\t\t: /demo support")
    print("Loaded command\t\t: /demo invite")

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
    currentVersion = ""
    user2 = guild.me
    for activity in user2.activities:
      if isinstance(activity, discord.CustomActivity):
        currentVersion = activity.state.split()[1]
        break
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
      name = "Current Version :",
      value = f"> ` {currentVersion} `",
      inline = True
    ).add_field(
      name = "Command Prefix :",
      value = "> ` demo.<command_name> `",
      inline = True
    ).add_field(
      name = "Guild Count :",
      value = f"> ` {len(self.bot.guilds):,} `",
      inline = True
    ).add_field(
      name = "User Count :",
      value = f"> ` {len(self.bot.users):,} `",
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

  @app_commands.command(
    name = "support",
    description = "Join Demo's support server"
  )
  async def demoSupport(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.response
    supportGuildID = 1171782661761671168
    guild = self.bot.get_guild(supportGuildID)
    description = ""
    if guild.description is not None:
      description = f"\n\n> {guild.description}"
    embed = discord.Embed(
      title = guild.name,
      description = f"""
Join {self.bot.user.mention}'s support guild for news, updates, reports, suggestions and / or feedbacks ! See you there !{description}
      """,
      color = 0x2b2d31
    ).add_field(
      name = "Member Count :",
      value = f"> {len(guild.members):,}",
      inline = True
    )
    if guild.icon is not None:
      embed.set_thumbnail(
        url = guild.icon.url
      )
    if guild.banner is not None:
      embed.set_image(
        url = guild.banner.url
      )
    view = ui.View().add_item(
      ui.Button(
        label = "Support Server",
        url = "https://discord.gg/mXSXzc4SJB"
      )
    )
    await response.send_message(
      embed = embed,
      view = view,
      ephemeral = True
    )

  @app_commands.command(
    name = "invite",
    description = "Invite Demo to your server"
  )
  async def demoInvite(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    invite = "https://discord.com/api/oauth2/authorize?client_id=1169799947021975633&permissions=1633832791110&scope=bot+applications.commands"
    embed = discord.Embed(
      title = self.bot.user.display_name,
      description = f"Want to try {self.bot.user.mention} in your server ? Invite him now !",
      color = 0x2b2d31
    ).set_thumbnail(
      url = self.bot.user.display_avatar
    )
    view = ui.View().add_item(
      ui.Button(
        label = "Invite",
        url = invite
      )
    )
    await response.send_message(
      embed = embed,
      view = view,
      ephemeral = True
    )

  @demoInfo.error
  @demoSupport.error
  @demoInvite.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Demo(bot))