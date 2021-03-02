from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from discord.ext.commands import when_mentioned_or, command, has_permissions
from ..db import db

PREFIX = ""
OWNER_IDS = [582552522292592640]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" >{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" >{cog} cog loaded successfully")

        print(" >setup completed with no errors")

    def run(self, version):
        self.VERSION = version

        print("RUNNING SETUP...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("RUNNING BOT...")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        channel = self.get_channel(719109017976307734)
        await channel.send(">> REMEMBER TO COMPLY WITH THE RULES TO NOT BE PUNISHED! :D <<")

    async def on_connect(self):
        print(" >bot connected to discord")

    async def on_disconnect(self):
        print(" >bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("SOMETHING WENT WRONG")
            channel = self.get_channel(790894990397538324)
            await channel.send("`AN ERROR OCURRED :/`", delete_after=4)

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("`COMMAND NOT FOUND :c`", delete_after=4)

        elif hasattr(exc, "original"):
            raise exc.original

        elif isinstance(exc, CommandOnCooldown):
            ctx.send(
                f"`COMMAND IS ON [{str(exc.cooldown.type).split('.')[-1]} COOLDOWN :C TRY AGAIN IN {exc.retry_after:,.2f} SECONDS`",
                delete_after=4)

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(718810320931389521)
            self.stdout = self.get_channel(791418571459657738)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            channel = self.get_channel(791418571459657738)

            embed = Embed(title="😊 BOT ONLINE! 😊", description="PolarBot connected to discord and is ready to use!",
                          colour=0xAAAAF4, timestamp=datetime.utcnow())
            fields = [("Name", "Value", True),
                      ("TO VIEW COMMANDS TYPE aHelp", "SEND THE COMMANDS IN THE CORRECT CHANNEL", True),
                      ("VISIT THE WEBPAGE!", "http://polarb.epizy.com", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Bot by Ander The Bear", icon_url=self.guild.icon_url)
            embed.set_footer(text="BOT ONLINE!")
            embed.set_thumbnail(url=self.guild.icon_url)
            await channel.send(embed=embed)

            # while not self.cogs_ready.all_ready():
            # await sleep(0.5)

            self.ready = True
            print("BOT READY ʕᵔᴥᵔʔ")

        else:
            print("BOT RECONNECTED")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
