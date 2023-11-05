import discord
import json
import traceback
from discord import app_commands, ui
from discord.ext import commands
from discord.utils import get

class UserCommands(commands.GroupCog, name = "user", description = "user commands"):
  def __init__(self, bot):
    self.bot = bot
    self.bot.tree.add_command(
      app_commands.ContextMenu(
        name = "User Profile",
        callback = self.get_profile
      )
    )
    self.bot.tree.add_command(
      app_commands.ContextMenu(
        name = "User Avatar",
        callback = self.get_avatar
      )
    )
    with open('json/emojis.json', 'r') as f:
      self.emojis = json.load(f)
    print("Loaded command group : user")
    print("Loaded command : /user profile")
    print("Loaded context menu : User Profile")

  async def get_profile(self, interaction : discord.Interaction, member : discord.Member):
    try:
      emojis = self.emojis
      user = interaction.guild.get_member(member.id)
      user2 = await self.bot.fetch_user(user.id)
      response = interaction.response
      desktopStatus = ""
      if user.desktop_status != discord.Status.offline:
        if user.desktop_status == discord.Status.online:
          desktopStatusIconId = emojis["desktop online"]
        elif user.desktop_status == discord.Status.do_not_disturb or user.desktop_status == discord.Status.dnd:
          desktopStatusIconId = emojis["desktop do not disturb"]
        elif user.desktop_status == discord.Status.idle:
          desktopStatusIconId = emojis["desktop idle"]
        desktopStatusIcon = self.bot.get_emoji(desktopStatusIconId)
        desktopStatus = f"{desktopStatusIcon} "
      webStatus = ""
      if user.web_status != discord.Status.offline:
        if user.web_status == discord.Status.online:
          webStatusIconId = emojis["web online"]
        elif user.web_status == discord.Status.dnd:
          webStatusIconId = emojis["web do not disturb"]
        elif user.web_status == discord.Status.idle:
          webStatusIconId = emojis["web idle"]
        webStatusIcon = self.bot.get_emoji(webStatusIconId)
        webStatus = f"{webStatusIcon} "
      mobileStatus = ""
      if user.mobile_status != discord.Status.offline:
        if user.mobile_status == discord.Status.online:
          mobileStatusIconId = emojis["mobile online"]
        elif user.mobile_status == discord.Status.dnd:
          mobileStatusIconId = emojis["mobile do not disturb"]
        elif user.mobile_status == discord.Status.idle:
          mobileStatusIconId = emojis["mobile idle"]
        mobileStatusIcon = self.bot.get_emoji(mobileStatusIconId)
        mobileStatus = f"{mobileStatusIcon}"
      userCustomStatus = ""
      if not user.bot:
        if len(user.activities) != 0:
          for activity in user.activities:
            if isinstance(activity, discord.CustomActivity):
              activityEmoji = ""
              activityName = ""
              if activity.emoji is not None:
                if activity.emoji.is_custom_emoji():
                  activityEmoji = self.bot.get_emoji(activity.emoji.id)
                  if activityEmoji is None:
                    activityEmoji = activity.emoji
                else:
                  activityEmoji = activity.emoji
              if activity.name is not None:
                activityName = f" {activity.name}"
              userCustomStatus = f"\n\n> {activityEmoji}{activityName}"
              break
      else:
        if user.activity is not None:
          if isinstance(user.activity, discord.CustomActivity):
            userCustomStatus = f"\n\n> {user.activity.state}"
          else:
            for activity in user.activities:
              if isinstance(activity, discord.CustomActivity):
                activityEmoji = ""
                activityName = ""
                if activity.emoji is not None:
                  if activity.emoji.is_custom_emoji():
                    activityEmoji = self.bot.get_emoji(activity.emoji.id)
                    if activityEmoji is None:
                      activityEmoji = activity.emoji
                  else:
                    activityEmoji = activity.emoji
                if activity.name is not None:
                  activityName = f" {activity.name}"
                userCustomStatus = f"\n\n> {activityEmoji}{activityName}"
                break
      userPublicFlagsStr = []
      userPublicFlagsList = user.public_flags.all()
      if not user.bot:
        for flag in userPublicFlagsList:
          if flag.name in emojis:
            flagIcon = self.bot.get_emoji(emojis[flag.name])
            userPublicFlagsStr.append(str(flagIcon))
      else:
        if user.public_flags.verified_bot:
          left = self.bot.get_emoji(emojis["verified_bot_left"])
          right = self.bot.get_emoji(emojis["verified_bot_right"])
          userPublicFlagsStr.append(f"{left}{right}")
        else:
          flagIcon = self.bot.get_emoji(emojis["bot"])
          userPublicFlagsStr.append(str(flagIcon))
      userPublicFlags = " ".join(userPublicFlagsStr)
      userNickname = f"\n*Nickname** : ` {user.nick} `" if user.nick is not None else ""
      embed = discord.Embed(
        title = f"{user.name} {desktopStatus}{webStatus}{mobileStatus}{userPublicFlags}",
        description = f"""
**User ID** : || ` {user.id} ` ||{userNickname}
**Created** : <t:{int(user.created_at.timestamp())}:R>
**Joined** : <t:{int(user.joined_at.timestamp())}:R>{userCustomStatus}
        """,
        color = 0x2b2d31
      ).set_thumbnail(
        url = user.display_avatar
      )
      if len(user.roles) - 1 != 0:
        userRolesCount = len(user.roles) - 1
        embed.add_field(
          name = "Roles :",
          value = f"> ` {userRolesCount:,} `",
          inline = True
        )
      if user.premium_since is not None:
        userBoostedSince = f"<t:{int(user.premium_since.timestamp())}:R>"
        embed.add_field(
          name = "Boosted the server since :",
          value = f"> {userBoostedSince}",
          inline = True
        )
      if user.timed_out_until is not None:
        embed.add_field(
          name = "Timed Out Until :",
          value = f"> <t:{int(user.timed_out_until.timestamp())}:R>",
          inline = True
        )
      if user2.banner is not None:
        embed.set_image(
          url = user2.banner.url
        )
      embeds = [embed]
      view = None
      for activity in user.activities:
        if activity.type == discord.ActivityType.playing:
          gameEmbedExists = False
          for embed in embeds:
            if embed.title == "Playing a Game":
              gameEmbedExists = True
              break
          if gameEmbedExists:
            continue
          try:
            activityDetails = f"\n**Details** : ` {activity.details} `" if activity.details is not None else ""
            activityState = f"\n**State** : ` {activity.state} `" if activity.state is not None else ""
            gameStart = f"\n**Start** : <t:{int(activity.start.timestamp())}:R>" if activity.start is not None else ""
            gameEnd = f"\n**End** : <t:{int(activity.end.timestamp())}:R>" if activity.end is not None else ""
            gameEmbed = discord.Embed(
              title = "Playing a Game",
              description = f"""
  **Name** : ` {activity.name} `{activityDetails}{activityState}{gameStart}{gameEnd}
              """,
              color = 0x2b2d31
            ).set_thumbnail(
              url = activity.large_image_url if activity.large_image_url is not None else activity.small_image_url
            )
          except:
            gameStart = f"\n**Start** : <t:{int(activity.start.timestamp())}:R>" if activity.start is not None else ""
            gameEnd = f"\n**End** : <t:{int(activity.end.timestamp())}:R>" if activity.end is not None else ""
            gameEmbed = discord.Embed(
              title = "Playing a Game",
              description = f"""
**Name** : ` {activity.name} ` {gameStart}{gameEnd}
              """,
              color = 0x2b2d31
            )
          embeds.append(gameEmbed)
        elif isinstance(activity, discord.Spotify):
          artistsList = [f"` {artist} `" for artist in activity.artists]
          artists = ", ".join(artistsList)
          spotifyIcon = self.bot.get_emoji(emojis["spotify"])
          spotifyEmbed = discord.Embed(
            title = f"Listening to {activity.title}",
            description = f"""
**Album** : ` {activity.album} `
**Artist(s)** : {artists}
            """,
            color = activity.color,
            url = activity.album_cover_url
          ).set_thumbnail(
            url = activity.album_cover_url
          )
          view = ui.View().add_item(
            ui.Button(
              label = f"Play on Spotify",
              emoji = spotifyIcon,
              url = activity.track_url
            )
          )
          embeds.append(spotifyEmbed)
      if view is None:
        await interaction.response.send_message(
          embeds = embeds
        )
      else:
        for ind, emb in enumerate(embeds):
          if emb.title.startswith("Listening to "):
            embeds.append(embeds.pop(ind))
            break
        await response.send_message(
          embeds = embeds,
          view = view
        )
    except:
      traceback.print_exc()

  @app_commands.command(
    name = "profile",
    description = "Retrieve a user's profile"
  )
  @app_commands.describe(
    member = "Select a member"
  )
  async def userProfile(self, interaction : discord.Interaction, member : discord.Member = None):
    await self.get_profile(interaction, member if member is not None else interaction.user)

  async def get_avatar(self, interaction : discord.Interaction, member : discord.Member):
    response = interaction.response
    if member.guild_avatar is not None:
      avatarUrl = member.guild_avatar.url
    elif member.avatar is not None:
      avatarUrl = member.avatar.url
    else:
      avatarUrl = member.display_avatar
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_author(
      name = member.display_name,
      icon_url = member.display_avatar
    ).set_image(
      url = avatarUrl
    )
    await response.send_message(
      embed = embed
    )

  @app_commands.command(
    name = "avatar",
    description = "Retrieve a user's avatar"
  )
  @app_commands.describe(
    member = "Select a member"
  )
  async def userAvatar(self, interaction : discord.Interaction, member : discord.Member = None):
    await self.get_avatar(interaction, member if member is not None else interaction.user)

async def setup(bot):
  await bot.add_cog(UserCommands(bot))