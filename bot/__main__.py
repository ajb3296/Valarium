import discord
import asyncio

from discord.ext import commands
from bot.background.read_varium import read_varium
from bot.background.broadcast import broadcast
from bot.background.reset_db import reset_db
from bot.utils.database import channelDataDB

from bot import LOGGER, TOKEN, EXTENSIONS, BOT_VER

async def status_task():
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game ("/help : 도움말"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
            channel_list = channelDataDB.get_on_channel()
            await bot.change_presence(
                activity = discord.Game (f"{len(channel_list)}개의 채널에 알림을 보내주고 있어요!"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
        except Exception:
            pass

class Bot (commands.Bot) :
    def __init__ (self) :
        super().__init__ (
            intents=intents
        )
        self.remove_command("help")

        for i in EXTENSIONS:
            self.load_extension("bot.cogs." + i)

    async def on_ready (self) :
        LOGGER.info(f"{self.user} | {BOT_VER}")
        await self.change_presence(
            activity = discord.Game ("/help : 도움말"),
            status = discord.Status.online,
        )
        bot.loop.create_task(status_task())
        bot.loop.create_task(read_varium())
        bot.loop.create_task(broadcast(bot))
        bot.loop.create_task(reset_db())

    async def on_message (self, message) :
        if message.author.bot:
            return
        await self.process_commands (message)

intents = discord.Intents().all()

bot = Bot()
bot.run(TOKEN)