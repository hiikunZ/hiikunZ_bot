# import discord
from discord.ext import commands

import os
import datetime


class Develop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log_channel = self.bot.get_channel(int(os.environ["LOG_CHANNEL_ID"]))
        await log_channel.send("Connected!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log_channel = self.bot.get_channel(int(os.environ["LOG_CHANNEL_ID"]))
        await log_channel.send(f"Error: {error}")

    @commands.Cog.listener()
    async def on_error(self, error):
        log_channel = self.bot.get_channel(int(os.environ["LOG_CHANNEL_ID"]))
        await log_channel.send(f"Error: {error}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        greeting_channel = self.bot.get_channel(int(os.environ["GREETING_CHANNEL_ID"]))
        await greeting_channel.send("こんにちは？新人さんですね？よろしくお願いします。")

    @commands.hybrid_command()
    async def ping(self, ctx):
        "応答確認用のコマンドです。"
        await ctx.send("pong!")

    @commands.hybrid_command()
    async def time(self, ctx):
        "現在の時刻を表示します。"
        JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
        await ctx.send(
            "現在の時刻は "
            + datetime.datetime.now(tz=JST).strftime("%Y/%m/%d %H:%M:%S")
            + " です。"
        )


async def setup(bot):
    await bot.add_cog(Develop(bot))
