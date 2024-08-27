from dotenv import load_dotenv

import os
import menuHandler
import kakaotalkHandler
import locale
import time

load_dotenv()
locale.setlocale(locale.LC_TIME, "ko_KR")
groupName = os.environ.get("GROUP_NAME")

if __name__ == '__main__':
    message = time.strftime("%Y년 %m월 %d일 %a요일 급식 알림\n\n") + menuHandler.get_lunch() + "\n\n" + menuHandler.get_desc()
    kakaotalkHandler.openChatroom(groupName)
    kakaotalkHandler.sendText(groupName, message)
    print(message)
