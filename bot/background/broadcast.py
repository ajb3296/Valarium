import discord
import asyncio
import traceback
import urllib.request
from datetime import datetime
from colorthief import ColorThief

from bot.utils.crawler import getJSON
from bot.utils.database import *
from bot.utils.language import i18n
from bot import LOGGER, BOT_VER, color_code

async def broadcast(bot):
    await asyncio.sleep(5)

    while True:
        try:
            now_datetime = datetime.now().timestamp()

            # 데이터 가져오기
            table_data = scheduleDB.get_database()

            if table_data is not None:
                # 테이블 내부 데이터 시간 체크 후 알림 전송
                for data in table_data:
                    # 이미 시간이 지났거나 지금이라면
                    if data[2] <= now_datetime:
                        LOGGER.info(f"Send msg : {data}")
                        await send_msg(bot, data)
                        status = scheduleDB.delete_db(data[0])
                        if status is True:
                            LOGGER.info(f"Data removal successful : {data}")
                        else:
                            LOGGER.info(f"Data removal failed, reset_db will delete it : {data}")

        except Exception:
            print(traceback.format_exc())
        await asyncio.sleep(30)

async def send_msg(bot, data):
    channel_id_list = channelDataDB.get_on_channel()
    if channel_id_list != None:
        url = data[1]
        unixtime = data[2]
        icon = data[3]

        # 색상 추출
        try:
            urllib.request.urlretrieve(icon, f"temp/{icon.split('/')[-1]}")
            dominant_color = ColorThief(f"temp/{icon.split('/')[-1]}").get_color(quality=1)
            hex_color = hex(dominant_color[0]) + hex(dominant_color[1])[2:] + hex(dominant_color[2])[2:]
            color = int(hex_color, 16)
        except Exception:
            color = color_code
        
        # 데이터 가져오기
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        yt_data = await getJSON(f"https://www.youtube.com/oembed?url={url}&format=json", header)
        title = yt_data['title']
        name = yt_data['author_name']
        thumbnail = yt_data['thumbnail_url']

        for channel_id in channel_id_list:
            target_channel = bot.get_channel(channel_id)
            try:
                embed=discord.Embed(title=title, description="", color=color)
                embed.add_field(name=i18n(channel_id, "broadcast", "버튜버"), value=name, inline=False)
                embed.add_field(name=i18n(channel_id, "broadcast", "방송 시간"), value=f"<t:{unixtime}>", inline=False)
                embed.add_field(name=i18n(channel_id, "broadcast", "링크"), value=url, inline=False)
                # 유튜버 프로필 설정
                embed.set_thumbnail(url=icon)
                # 썸네일 설정
                embed.set_image(url=thumbnail)
                embed.set_footer(text=f"{bot.user} | {BOT_VER}")
                msg = await target_channel.send(embed=embed)
                if target_channel.type == discord.ChannelType.news:
                    await msg.publish()
            except Exception:
                print(traceback.format_exc())