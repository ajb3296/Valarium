# Valarium

Varium 알리미 개발 의뢰를 받아 개발했다.

## 봇 초대

https://discord.com/api/oauth2/authorize?client_id=1057656763962372157&permissions=8&scope=bot%20applications.commands

## How to install
1. bot 폴더 안에 config.py 파일을 만든다.
2. config.py 파일을 아래와 같이 작성한다.
```python
from bot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    DebugServer = [디버그 서버 id]
```
`sample_config.py`를 참고하여 만들면 된다.<br>
3. `python3 -m bot` 명령어로 실행한다.