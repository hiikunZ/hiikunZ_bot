import discord
from discord.ext import commands, tasks

import datetime
import os

from cogs.utils.contestdata import ContestData
import cogs.utils.atcoder as atcoder
import cogs.utils.codeforces as codeforces
import cogs.utils.yukicoder as yukicoder
import cogs.utils.codechef as codechef

JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
time = datetime.time(hour=6, minute=0, tzinfo=JST)

mentions = {
    "AtCoder": "<@&" + os.environ["ATCODER_ROLE_ID"] + ">",
    "Codeforces": "<@&" + os.environ["CODEFORCES_ROLE_ID"] + ">",
    "yukicoder": "<@&" + os.environ["YUKICODER_ROLE_ID"] + ">",
    "CodeChef": "<@&" + os.environ["CODECHEF_ROLE_ID"] + ">",
}


class Contest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_run = None
        self.contest_batch.start()
        self.thread_batch.start()

    def create_embed(self, data: ContestData):
        now = datetime.datetime.now(tz=JST)
        now = datetime.datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            tzinfo=JST,
        )
        embed = discord.Embed(title=data.Type, url=data.Url, color=data.Color)
        embed.set_author(name=data.Name, url=data.Url, icon_url=data.Platformimage)
        if data.Starttime.date() == now.date():
            embed.set_thumbnail(url="https://i.imgur.com/HMOxSxt.png")
        elif data.Starttime.date() == now.date() + datetime.timedelta(days=1):
            embed.set_thumbnail(url="https://i.imgur.com/VQ5l5Ug.png")
        if data.Starttime.date() != data.Endtime.date():
            timeinfo = (
                data.Starttime.strftime("%Y-%m-%d(%a) %H:%M")
                + " ~ "
                + data.Endtime.strftime("%Y-%m-%d(%a) %H:%M")
            )
        else:
            timeinfo = (
                data.Starttime.strftime("%Y-%m-%d(%a) %H:%M")
                + " ~ "
                + data.Endtime.strftime("%H:%M")
            )
        timeinfo += " (" + str(data.Duration)[:-3] + ")"
        if data.Status == "Running":
            timeinfo += "\nTime remaining : " + str(data.Endtime - now)[:-3]
        otherinfo = "rated : " + data.RatedRange + "\n[standings](" + data.StandingsUrl + ")"
        if data.ProblemAUrl is not None:
            otherinfo += " [problem_A](" + data.ProblemAUrl + ")"
        embed.add_field(
            name=timeinfo,
            value=otherinfo
        )
        return embed

    @tasks.loop(time=time)
    async def contest_batch(self):
        now = datetime.datetime.now(tz=JST)
        now = datetime.datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            tzinfo=JST,
        )
        contest_channel = self.bot.get_channel(int(os.environ["CONTEST_CHANNEL_ID"]))
        notice_channel = self.bot.get_channel(int(os.environ["NOTICE_CHANNEL_ID"]))
        data = []
        data.extend(atcoder.get_contest_data())
        data.extend(codeforces.get_contest_data())
        data.extend(yukicoder.get_contest_data())
        data.extend(codechef.get_contest_data())
        data.sort(key=lambda x: x.Starttime)
        await notice_channel.send("Running contests")
        ok = False
        for contest in data:
            if contest.Status == "Running":
                embed = self.create_embed(contest)
                await notice_channel.send(embed=embed)
                ok = True
        if not ok:
            await notice_channel.send("=== There is no running contests ===")
        await notice_channel.send("Upcoming contests")
        for contest in data:
            if contest.Status == "Upcoming":
                embed = self.create_embed(contest)
                await notice_channel.send(embed=embed)
        made = []
        threads = contest_channel.threads
        for thread in threads:
            made.append(thread.name)
        for contest in data:
            if (
                contest.Status == "Upcoming"
                and contest.Starttime - now <= datetime.timedelta(days=1)
            ):
                if contest.Name in made:
                    threads = contest_channel.threads
                    for thread in threads:
                        if thread.name == contest.Name:
                            embed = self.create_embed(contest)
                            await thread.send(embed=embed)
                            break
                else:
                    made.append(contest.Name)
                    thread = await contest_channel.create_thread(
                        name=contest.Name,
                        auto_archive_duration=1440,
                        type=discord.ChannelType.public_thread,
                    )
                    embed = self.create_embed(contest)
                    await thread.send(embed=embed)

    @tasks.loop(seconds=10)
    async def thread_batch(self):
        now = datetime.datetime.now(tz=JST)
        now = datetime.datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            tzinfo=JST,
        )
        if self.last_run == now:
            return
        contest_channel = self.bot.get_channel(int(os.environ["CONTEST_CHANNEL_ID"]))
        if contest_channel is None:  # 起動直後にNoneになることがある
            return
        self.last_run = now
        threads = contest_channel.threads
        data = []
        data.extend(atcoder.get_contest_data())
        data.extend(codeforces.get_contest_data())
        data.extend(yukicoder.get_contest_data())
        data.extend(codechef.get_contest_data())
        data.sort(key=lambda x: x.Starttime)
        send = []
        for contest in data:
            if contest.Status == "Upcoming":
                if contest.Starttime - now == datetime.timedelta(minutes=120):
                    for thread in threads:
                        if thread.name == contest.Name:
                            embed = self.create_embed(contest)
                            if not contest.Name in send:
                                await thread.send(
                                    "2 hours left " + mentions[contest.Platform]
                                )
                                send.append(contest.Name)
                            await thread.send(embed=embed)
                            if "(" in contest.Name or "（" in contest.Name:
                                await thread.send(
                                    "**It may take some time to register, so you'd better do it early!**"
                                )
                            break
                if contest.Starttime - now == datetime.timedelta(minutes=60):
                    for thread in threads:
                        if thread.name == contest.Name:
                            embed = self.create_embed(contest)
                            if not contest.Name in send:
                                await thread.send(
                                    "1 hour left " + mentions[contest.Platform]
                                )
                                send.append(contest.Name)
                            await thread.send(embed=embed)
                            if "(" in contest.Name or "（" in contest.Name:
                                await thread.send(
                                    "**It may take some time to register, so you'd better do it early!**"
                                )
                            break
                if contest.Starttime - now == datetime.timedelta(minutes=30):
                    for thread in threads:
                        if thread.name == contest.Name:
                            embed = self.create_embed(contest)
                            if not contest.Name in send:
                                await thread.send(
                                    "30 minutes left " + mentions[contest.Platform]
                                )
                                send.append(contest.Name)
                            await thread.send(embed=embed)
                            if "(" in contest.Name or "（" in contest.Name:
                                await thread.send(
                                    "**It may take some time to register, so you'd better do it early!**"
                                )
                            break
                if contest.Starttime - now == datetime.timedelta(minutes=10):
                    for thread in threads:
                        if thread.name == contest.Name:
                            embed = self.create_embed(contest)
                            if not contest.Name in send:
                                await thread.send(
                                    "10 minutes left " + mentions[contest.Platform]
                                )
                                send.append(contest.Name)
                            await thread.send(embed=embed)
                            if "(" in contest.Name or "（" in contest.Name:
                                await thread.send(
                                    "**It may take some time to register, so you'd better do it early!**"
                                )
                            break
            elif contest.Status == "Finished":
                if contest.Endtime == now:
                    for thread in threads:
                        if thread.name == contest.Name:
                            embed = self.create_embed(contest)
                            await thread.send("Contest finished")
                            break

    @commands.hybrid_command()
    async def contest(self, ctx):
        "コンテスト情報をまとめて表示します。"
        await ctx.send("Running contests")
        data = []
        data.extend(atcoder.get_contest_data())
        data.extend(codeforces.get_contest_data())
        data.extend(yukicoder.get_contest_data())
        data.extend(codechef.get_contest_data())
        data.sort(key=lambda x: x.Starttime)
        ok = False
        for contest in data:
            if contest.Status == "Running":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)
                ok = True
        if not ok:
            await ctx.channel.send("=== There is no running contests ===")
        await ctx.channel.send("Upcoming contests")
        for contest in data:
            if contest.Status == "Upcoming":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)

    @commands.hybrid_command()
    async def atcoder(self, ctx):
        "AtCoderのコンテスト情報を表示します。"
        await ctx.send("Running contests")
        data = atcoder.get_contest_data()
        data.sort(key=lambda x: x.Starttime)
        ok = False
        for contest in data:
            if contest.Status == "Running":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)
                ok = True
        if not ok:
            await ctx.channel.send("=== There is no running contests ===")
        await ctx.channel.send("Upcoming contests")
        for contest in data:
            if contest.Status == "Upcoming":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)

    @commands.hybrid_command()
    async def codeforces(self, ctx):
        "Codeforcesのコンテスト情報を表示します。"
        await ctx.send("Running contests")
        data = codeforces.get_contest_data()
        data.sort(key=lambda x: x.Starttime)
        ok = False
        for contest in data:
            if contest.Status == "Running":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)
                ok = True
        if not ok:
            await ctx.channel.send("=== There is no running contests ===")
        await ctx.channel.send("Upcoming contests")
        for contest in data:
            if contest.Status == "Upcoming":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)

    @commands.hybrid_command()
    async def yukicoder(self, ctx):
        "yukicoderのコンテスト情報を表示します。"
        await ctx.send("Running contests")
        data = yukicoder.get_contest_data()
        data.sort(key=lambda x: x.Starttime)
        ok = False
        for contest in data:
            if contest.Status == "Running":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)
                ok = True
        if not ok:
            await ctx.channel.send("=== There is no running contests ===")
        await ctx.channel.send("Upcoming contests")
        for contest in data:
            if contest.Status == "Upcoming":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)

    @commands.hybrid_command()
    async def codechef(self, ctx):
        "CodeChefのコンテスト情報を表示します。"
        await ctx.send("Running contests")
        data = codechef.get_contest_data()
        data.sort(key=lambda x: x.Starttime)
        ok = False
        for contest in data:
            if contest.Status == "Running":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)
                ok = True
        if not ok:
            await ctx.channel.send("=== There is no running contests ===")
        await ctx.channel.send("Upcoming contests")
        for contest in data:
            if contest.Status == "Upcoming":
                embed = self.create_embed(contest)
                await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Contest(bot))
