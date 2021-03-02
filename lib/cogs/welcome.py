from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        await self.bot.get_channel(790894970637647882).sendf("Welcome to **{member.guild.name}** {member.mention}!")

        try:
            await member.send(f"WELCOME TO **{member.guild.name}**! YOU ARE NOW A COOL POLAR BEAR! `YOUTUBE =>` https://cutt.ly/wh0JPOV")

        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        pass


def setup(bot):
    bot.add_cog(Welcome(bot))