import time
import schedule
import random
import notice_manually

def job():
    time.sleep(random.randint(1, 5))
    notice_manually.main()

schedule.every().day.at("07:00", "Asia/Seoul").do(job())
