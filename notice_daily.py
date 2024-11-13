import time
import schedule
import random
import notice_manually
from datetime import datetime

def job():
    if datetime.today().weekday() < 5:
        time.sleep(random.randint(1, 5) * 60)
        notice_manually.main()

def still_alive():
    print(f"Still alive at {datetime.today()}")

schedule.every(1).day.at("07:00", "Asia/Seoul").do(job)
schedule.every(1).hours.do(still_alive)

while True:
    schedule.run_pending()
    time.sleep(1)