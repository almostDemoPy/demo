import asyncio
import discord
import os
import traceback
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
  command_prefix = "demo.",
  help_command = None,
  intents = discord.Intents.all(),
  activity = discord.Activity(
    type = discord.ActivityType.custom,
    name = " ",
    state = "Version 5.1.1"
  )
)

async def load():
  for folder in os.listdir('cogs'):
    for file in os.listdir(f'cogs/{folder}'):
      if file.endswith('.py'):
        await bot.load_extension(
          f'cogs.{folder}.{file[:-3]}'
        )

async def main():
  await load()
  async with bot:
    await bot.start(
      os.getenv("token")
    )

try:
  asyncio.run(main())
except:
  traceback.print_exc()