#
# (name, (datetime, unixdatetime, isLive, url, thumbnail, title, talent.iconImageUrl))
#

import asyncio
import traceback
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from bot.utils.crawler import getText
from bot.utils.database import *
from bot import schedule_link

async def read_varium():
    while True:
        try:
            today = datetime.today()
            now_unix_time = int(datetime.now().timestamp())

            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            result = await getText(schedule_link, header)
            soup = BeautifulSoup(result, "lxml")
            today_list = soup.find("div", {"class": "today wrapper"}).find_all("li")
            tommorow_list = soup.find("div", {"class": "tommorow wrapper"}).find_all("li")                

            goto_DB = []
            for broadcast in today_list:
                # 과거일 경우 추가하지 않음
                unixtime = int(datetime.strptime(str(today.year) + "/" + broadcast.find("div", {"class": "pink date"}).get_text(), '%Y/%m/%d %H:%M').timestamp())
                if unixtime > now_unix_time:
                    link = broadcast.find("a")["href"]
                    iconImage = schedule_link.replace("schedule.html", "") + broadcast.find("div", {"class": "talents"}).find("img")["src"]
                    goto_DB.append((link, unixtime, iconImage))
            
            for broadcast in tommorow_list:
                # 과거일 경우 추가하지 않음
                unixtime = int(datetime.strptime(str((today + timedelta(days=1)).year) + "/" + broadcast.find("div", {"class": "pink date"}).get_text(), '%Y/%m/%d %H:%M').timestamp())
                if unixtime > now_unix_time:
                    link = broadcast.find("a")["href"]
                    iconImage = schedule_link.replace("schedule.html", "") + broadcast.find("div", {"class": "talents"}).find("img")["src"]
                    goto_DB.append((link, unixtime, iconImage))

            scheduleDB.set_database(goto_DB)

        except Exception:
            print(traceback.format_exc())
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import requests
    schedule_link = "https://varium.jp/schedule.html"
    read_varium()