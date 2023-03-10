import os
import sys
import logging
import sqlite3

# Bot version
BOT_VER = "V.1.0"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("3.6 버전 이상의 Python 이 있어야 합니다. 여러 기능이 해당 Python3.6 버전을 따릅니다. 봇 종료.")
    quit(1)

from bot.config import Development as Config

TOKEN            = Config.TOKEN
OWNERS           = Config.OWNERS
DebugServer      = Config.DebugServer
color_code       = Config.color_code
schedule_link    = Config.schedule_link
schedule_db_path = Config.schedule_db_path
channel_db_path  = Config.channel_db_path

EXTENSIONS = []
for file in os.listdir("bot/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))