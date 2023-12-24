import asyncio
import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnMessageEdit(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: on_message_edit")

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    try:
      guild = before.guild
      author = before.author
      if get_config(guild.id):
        config = Config(guild)
        if config.logs.on_message_edit.channel_id is not None:
          channel = self.bot.get_channel(config.logs.on_message_edit.channel_id)
          webhooks = await channel.webhooks()
          if not webhooks:
            webhook = await channel.create_webhook(
              name = self.bot.user.display_name,
              avatar = await self.bot.user.display_avatar.read()
            )
          else:
            for wh in webhooks:
              if wh.user == self.bot.user:
                webhook = wh
                break
          beforeEmbed = discord.Embed(
            title = "Before :",
            description = "` No content provided `" if before.content == "" else before.content,
            color = 0x2b2d31
          )
          if before.attachments:
            beforeEmbed.add_field(
              name = "Attachments :",
              value = ">>> " + "\n".join([attachment.url for attachment in before.attachments]),
              inline = False
            )
          afterEmbed = discord.Embed(
            title = "After :",
            description = after.content if after.content != "" else "` No content provided `",
            color = 0x2b2d31
          )
          if after.attachments:
            afterEmbed.add_field(
              name = "Attachments :",
              value = ">>> " + "\n".join([attachment.url for attachment in after.attachments]),
              inline = True
            )
          view = ui.View().add_item(
            ui.Button(
              label = "Jump to Message",
              url = before.jump_url
            )
          )
          await webhook.send(
            embeds = [beforeEmbed, afterEmbed],
            view = view,
            username = author.display_name,
            avatar_url = author.display_avatar
          )
    except:
      traceback.print_exc()

async def setup(bot):
  await bot.add_cog(OnMessageEdit(bot))