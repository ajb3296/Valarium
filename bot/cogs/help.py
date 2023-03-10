import discord
from discord.ext import commands
from discord.commands import slash_command, Option

from bot import LOGGER, BOT_VER, color_code, EXTENSIONS
from bot.utils.language import i18n

class Help (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def help (self, ctx, *, help_option : Option(str, "알고 싶은 메뉴를 선택하세요.", choices=["GENERAL", "ALARM", "VOICE"])) :
        """ 도움말 """
        if not help_option == None:
            help_option = help_option.upper()
        if help_option == "GENERAL" or help_option == "일반":
            embed=discord.Embed(title=i18n(ctx.author.id, "help", "기본적인 명령어"), color=color_code)

            if "about" in EXTENSIONS:
                embed.add_field(name=f"/about",  value=f">>> {i18n(ctx.author.id, 'help', '봇에 대한 정보를 알려드립니다.')}", inline=True)

            if "other" in EXTENSIONS:
                embed.add_field(name=f"/invite", value=f">>> {i18n(ctx.author.id, 'help', '당신이 타 서버의 관리자라면 저를 해당 서버에 초대할 수 있습니다.')}", inline=True)
                embed.add_field(name=f"/uptime", value=f">>> {i18n(ctx.author.id, 'help', '서버의 업타임을 알려드립니다.')}", inline=True)

            if "ping" in EXTENSIONS:
                embed.add_field(name=f"/ping",   value=f">>> {i18n(ctx.author.id, 'help', '핑 속도를 측정합니다.')}", inline=True)

            embed.set_footer(text=f"{self.bot.user} | {BOT_VER}")
            await ctx.respond(embed=embed)

        elif help_option == "ALARM" or help_option == "알람":
            embed=discord.Embed(title=i18n(ctx.author.id, "help", "알람 명령어"), color=color_code)
            embed.add_field(name=f"/alarmstatus",         value=i18n(ctx.author.id, 'help', "해당 채널의 알람 상태를 알려드립니다."), inline=False)
            embed.add_field(name=f"/alarmset [*ON/OFF*]", value=i18n(ctx.author.id, 'help', "해당 채널에 알람을 설정하거나 해제합니다. 이는 서버의 관리자만이 사용할 수 있습니다."), inline=False)
            embed.set_footer(text=f"{self.bot.user} | {BOT_VER}")
            await ctx.respond(embed=embed)

        else:
            embed=discord.Embed(title=i18n(ctx.author.id, "help", "도움말"), description=i18n(ctx.author.id, 'help', "안녕하세요. 전 {bot_name} 입니다. 아래에 있는 명령어들을 이용해 도움말을 보세요.").format(bot_name=self.bot.user.name), color=color_code)
            embed.add_field(name=f"/help general", value=f">>> {i18n(ctx.author.id, 'help', '기본적인 명령어들을 알려드립니다.')}", inline=False)
            embed.add_field(name=f"/help alarm",   value=f">>> {i18n(ctx.author.id, 'help', '브이아리움 스케쥴 알람에 관한 명령어들을 보내드립니다.')}", inline=False)
            embed.add_field(name=f"/help voice",   value=f">>> {i18n(ctx.author.id, 'help', '음성채널에 관한 명령어들을 보내드립니다.')}", inline=False)
            embed.set_footer(text=f"{self.bot.user} | {BOT_VER}")
            await ctx.respond(embed=embed)
            

def setup (bot) :
    bot.add_cog (Help (bot))
    LOGGER.info('Help loaded!')