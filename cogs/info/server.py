import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands

class Server(commands.GroupCog, name = "server", description = "Server commands"):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command : /server info")

  @app_commands.command(
    name = "info",
    description = "Retrieve the current server's info"
  )
  async def serverInfo(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    guild = interaction.guild
    guildDescription = f"> {guild.description}\n\n" if guild.description is not None else ""
    guildOwner = guild.owner.mention if guild.owner is not None else self.bot.get_user(guild.owner_id).mention
    guildRoles = ""
    if len([role for role in guild.roles if not role.is_bot_managed() and not role.is_default()]) != 0:
      guildRolesCount = len([role for role in guild.roles if not role.is_bot_managed() and not role.is_default()])
      guildRoles = f"\n**Roles** : ` {guildRolesCount:,} `"
    vanityCode = f"\n**Vanity Code** : ` {guild.vanity_url_code} `" if guild.vanity_url_code is not None else ""
    guildScheduledEvents = ""
    if len(guild.scheduled_events) != 0:
      guildScheduledEvents = f"\n**Scheduled Events** : ` {(len(guild.scheduled_events)):,} `"
    guildCategories = f"> Categories : ` {(len(guild.categories)):,} `\n" if len(guild.categories) != 0 else ""
    guildForums = f"> Forums : ` {(len(guild.forums)):,} `\\n" if len(guild.forums) != 0 else ""
    guildStages = f"> Stages : ` {(len(guild.stage_channels)):,} `\n" if len(guild.stage_channels) != 0 else ""
    guildTexts = f"> Texts : ` {(len(guild.text_channels)):,} `\n" if len(guild.text_channels) != 0 else ""
    guildVoices = f"> Voices : ` {(len(guild.voice_channels)):,} `" if len(guild.voice_channels) != 0 else ""
    embed = discord.Embed(
      title = guild.name,
      description = f"""
{guildDescription}**Owner** : {guildOwner}
**Owner ID** : || ` {guild.owner_id} ` ||
**Created** : <t:{int(guild.created_at.timestamp())}:R>{guildRoles}{vanityCode}
**Rules Channel** : {guild.rules_channel.mention if guild.rules_channel is not None else "` None `"}{guildScheduledEvents}
      """,
      color = 0x2b2d31
    ).add_field(
      name = f"Channels : {(len(guild.channels)):,}",
      value = f"""
{guildCategories}{guildForums}{guildStages}{guildTexts}{guildVoices}
      """,
      inline = True
    ).add_field(
      name = f"Members : {(len(guild.members)):,}",
      value = f"""
> Humans : ` {(len([member for member in guild.members if not member.bot])):,} `
> Bots : ` {(len([member for member in guild.members if member.bot])):,} `
      """,
      inline = True
    )
    if len(guild.emojis) != 0:
      embed.add_field(
        name = f"Emojis :",
        value = f"> ` {(len(guild.emojis)):,} ` / ` {(guild.emoji_limit):,} `",
        inline = True
      )
    if len(guild.stickers) != 0:
      embed.add_field(
        name = f"Stickers :",
        value = f"> ` {(len(guild.stickers)):,} ` / ` {(guild.sticker_limit):,} `",
        inline = True
      )
    if guild.premium_subscription_count != 0:
      subscriberRole = f"\n> **Booster Role** : {guild.premium_subscriber_role.mention}" if guild.premium_subscriber_role is not None else ""
      embed.add_field(
        name = f"Boosts : {(guild.premium_subscription_count):,}",
        value = f"""
> Boost Level : ` {guild.premium_tier} `
> Booster(s) : ` {(len(guild.premium_subscribers)):,} `{subscriberRole}
        """,
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
    await response.send_message(
      embed = embed
    )

  @serverInfo.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Server(bot))