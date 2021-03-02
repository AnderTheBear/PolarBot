from random import choice, randint
from typing import Optional

from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["Hello", "hi", "Hi"], hidden=True)
    @cooldown(1, 5, BucketType.user)
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Whats Up', 'Yoo', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @command(name="echo", aliases=["Echo", "Say", "say"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
