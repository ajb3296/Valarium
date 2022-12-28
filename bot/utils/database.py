"""

id, url, unixdatetime, iconImage

"""

import sqlite3

from bot import schedule_db_path, channel_db_path

class scheduleDB:
    def set_database(broadcast_list):
        # Create table if it doesn't exist
        conn = sqlite3.connect(schedule_db_path, isolation_level=None)
        c = conn.cursor()

        # add broadcast data
        for broadcast in broadcast_list:
            link = broadcast[0]
            unixtime = broadcast[1]
            iconImage = broadcast[2]

            c.execute(f"CREATE TABLE IF NOT EXISTS alarm (id integer PRIMARY KEY AUTOINCREMENT, url text, unixdatetime int, iconImage text)")
            try:
                c.execute(f"SELECT * FROM alarm WHERE url=:url", {"url": link})
                temp = c.fetchone()
            except:
                temp = None
            if temp is None:
                # 없으면 추가
                c.execute(f"INSERT INTO alarm (url, unixdatetime, iconImage) VALUES(?, ?, ?)", (link, unixtime, iconImage))
        conn.close()

    def get_database():
        # 모든 데이터베이스 가져오기
        conn = sqlite3.connect(schedule_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM alarm ORDER BY id")
        except:
            conn.close()
            return None
        temp = c.fetchall()
        conn.close()
        return temp

    def get_database_from_id(id):
        # id로 데이터베이스 가져오기
        conn = sqlite3.connect(schedule_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM alarm WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_table_list():
        # 테이블 리스트 가져오기
        conn = sqlite3.connect(schedule_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = cursor.fetchall()
        cursor.close()
        tables = []
        for table in table_list:
            tables.append(table[0])
        return tables

    def delete_db(id):
        # 데이터 제거
        conn = sqlite3.connect(schedule_db_path, isolation_level=None)
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM alarm WHERE id = :ID",{"ID": id})
        except:
            cursor.close()
            return False
        cursor.close()
        return True

    def get_latest_data():
        # 마지막 행 리턴
        all_db = scheduleDB.get_database("alarm")
        if all_db is None:
            return None
        else:
            return all_db[-1]

class channelDataDB:
    def channel_status_set(id: int, status: str, language: str):
        # Create table if it doesn't exist
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS broadcastChannel (id integer PRIMARY KEY, onoff text, language text)")
        try:
            c.execute("SELECT * FROM broadcastChannel WHERE id=:id", {"id": id})
            a = c.fetchone()
        except:
            a = None
        if a is None:
            # add channel set
            c.execute(f"INSERT INTO broadcastChannel VALUES('{id}', '{status}', '{language}')")
        else:
            # modify channel set
            c.execute("UPDATE broadcastChannel SET onoff=:onoff, language=:language WHERE id=:id", {"onoff": status, "language": language, 'id': id})
        conn.close()

    def get_on_channel():
        # 모든 알람설정 되어있는 채널 가져오기
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM broadcastChannel ORDER BY id")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()

        on_channel = []
        for channel in temp:
            if channel[1] == "on":
                on_channel.append(channel[0])
        return on_channel

    def get_database_from_id(id: int):
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM broadcastChannel WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

if __name__ == "__main__":
    schedule_db_path = "holo.db"
    channel_db_path = "channel.db"
    post_list = [(80000, '제목1', '글쓴이1'), (80001, '제목2', '글쓴이2')]
    scheduleDB.set_database(post_list)