import discord
from discord.ext import commands

import asyncio
import os

from keep_alive import keep_alive

intents = discord.Intents.all()
intents.typing = False

bot = commands.Bot(command_prefix="!h ", intents=intents)
extensions = ["cogs.develop", "cogs.contest"]


@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"Error: {e}")


async def load_extensions():
    for extension in extensions:
        await bot.load_extension(extension)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.environ["DISCORD_BOT_TOKEN"])


keep_alive()

asyncio.run(main())
