import discord
import traceback
from assets.db import *
from discord import app_commands, ui
from discord.ext import commands

class OnMessageDelete(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event listener\t: on_message_delete")

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    try:
      guild = message.guild
      author = message.author
      if author.bot:
        return
      if get_config(guild.id):
        config = Config(guild)
        if config.logs.on_message_delete.channel_id is not None:
          channel = self.bot.get_channel(config.logs.on_message_delete.channel_id)
          webhooks = await channel.webhooks()
          if message.webhook_id is not None:
            msgChannel = message.channel
            msgChannelWebhooks = await msgChannel.webhooks()
            for wh in msgChannelWebhooks:
              if wh.id == message.webhook_id:
                if wh.user == self.bot.user:
                  return
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
          view = None
          if message.components:
            view = ui.View.from_message(
              message,
              timeout = None
            )
          await webhook.send(
            username = author.display_name,
            avatar_url = author.display_avatar,
            content = message.content,
            files = [await attachment.to_file() for attachment in message.attachments],
            embeds = message.embeds
          )
    except:
      traceback.print_exc()

async def setup(bot):
  await bot.add_cog(OnMessageDelete(bot))