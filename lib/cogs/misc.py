from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions

from ..db import db


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix", aliases=["Prefix"])
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("`THE PREFIX CANNOT BE MORE THAN 5 CHARACTERS`", delete_after=4)

        else:
            db.execute("UPDATE guilds SET PREFIX = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"`PREFIX SET TO {new}`")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("`YOU NEED THE -MANAGE SERVER- PERMISSION TO DO THAT :/`", delete_after=4)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


def setup(bot):
    bot.add_cog(Misc(bot))
