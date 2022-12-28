import asyncio
import traceback
from datetime import datetime

from bot import LOGGER
from bot.utils.database import *

async def reset_db():
    # 알림 전송 오류를 해결하기 위한 1시간 지난 데이터 제거
    await asyncio.sleep(120)
    while True:
        try:
            now_unix_time = int(datetime.now().timestamp())
            # 데이터 가져오기
            db_data = scheduleDB.get_database()
            if db_data is not None:
                for data in db_data:
                    # 이미 시간이 1시간 이상 지났다면
                    if int(data[2]) + 3600 < now_unix_time:
                        # 과거의 알림일 경우 제거 시도
                        for a in range(1, 4):
                            LOGGER.info(f"Try remove by db management system {a}th : {data}")
                            status = scheduleDB.delete_db(data[0])
                            LOGGER.info(f"Removed by db management system : {data}")
                            if status is True:
                                break
        except Exception:
            print(traceback.format_exc())
        await asyncio.sleep(120)