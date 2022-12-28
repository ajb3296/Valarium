import discord
from discord.ext import commands
from discord.commands import slash_command

from bot import LOGGER, BOT_VER, color_code

class About (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def about (self, ctx) :
        """ 봇에 대한 소개 """
        embed=discord.Embed(title="봇 정보", description="브이아리움 스케쥴 알리미", color=color_code)
        embed.add_field(name="Developer", value="천상의나무", inline=True)
        embed.add_field(name="관련 링크", value="[Github](https://github.com/ajb3296/Valarium)\n[Varium schedule](https://varium.jp/schedule.html#today)", inline=True)
        embed.set_footer(text=f"{self.bot.user} | {BOT_VER}")
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')