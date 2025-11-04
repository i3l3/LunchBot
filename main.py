from dotenv import load_dotenv
from PIL import Image, ImageFilter
from locale import setlocale
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler
from api_wrapper import get_meals, upload_post, upload_story
from image_maker import crop_img, write_text
import locale
import datetime
import os
import logging
import sys
import signal


setlocale(locale.LC_TIME, "ko_KR")
load_dotenv()
meal_name = ["조식", "중식", "석식"]

bottom = ("- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다.\n"
        "- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀,\n"
        "   7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산류,\n"
        "   14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣\n"
        "- 알레르기 정보는 게시글 설명란에 있습니다.")

def upload(date: datetime.date, code: list, offset: int, bg: str, ratio=4/5, is_post=True, is_test=False):
    # code: 조식, 중식, 석식 불러오기
    # 1: 조식 2: 중식 3: 석식
    if is_test:
        post_bg = crop_img(Image.open(bg), ratio).filter(ImageFilter.GaussianBlur(3))
        post_bg = write_text(post_bg, offset, ratio, "테스트 게시물", "테스트 게시물입니다.", bottom)
        post_bg.save("assets/post.jpg")

        if is_post:
            upload_post(["assets/post.jpg"], "테스트 게시물입니다.")
        elif not is_post:
            upload_story("assets/post.jpg")
        os.remove("assets/post.jpg")
        return

    meals = get_meals(date.strftime("%Y%m%d"))
    results = []
    title = date.strftime(f"%m월 %d일 %A 급식 정보")
    main = '\n\n'
    for i, meal in enumerate(meals):
        meal_code = int(meal["MMEAL_SC_CODE"])
        if meal_code in code:
            menu = meals[i]["DDISH_NM"].replace("<br/>", "\n")
            main += f'{meal_name[meal_code - 1]}\n{menu}\n\n'

            post_bg = crop_img(Image.open(bg), ratio).filter(ImageFilter.GaussianBlur(3))
            post_bg = write_text(post_bg, offset, ratio, title, menu, bottom)
            post_bg.save(f"assets/post{i}.jpg")
            results.append(f"assets/post{i}.jpg")

    # webhook logging?
    if is_post:
        upload_post(results, f"{title}{main}{bottom}")
    elif not is_post:
        for result in results:
            upload_story(result)

    for result in results:
        os.remove(result)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scheduler.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)

    '''
    금일 07:00 중식 스토리
    금일 16:30 석식 스토리
    명일 21:00 중식, 석식 포스트
    '''
    bg = "assets/boram1.png"
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)


    def lunch_story():
        try:
            logger.info("Starting lunch story upload")
            upload(today, [2], 50, bg, ratio=9 / 16, is_post=False)
            logger.info("Lunch story upload completed successfully")
        except Exception as e:
            logger.error(f"Error occurred during lunch story upload: {str(e)}", exc_info=True)
            raise


    def dinner_story():
        try:
            logger.info("Starting dinner story upload")
            upload(today, [3], 50, bg, ratio=9 / 16, is_post=False)
            logger.info("Dinner story upload completed successfully")
        except Exception as e:
            logger.error(f"Error occurred during dinner story upload: {str(e)}", exc_info=True)
            raise


    def meal_post():
        try:
            logger.info("Starting meal post upload")
            upload(tomorrow, [2, 3], 50, bg)
            logger.info("Meal post upload completed successfully")
        except Exception as e:
            logger.error(f"Error occurred during meal post upload: {str(e)}", exc_info=True)
            raise

    def test_post():
        try:
            logger.info("Starting test post upload")
            upload(today, [2], 50, bg, ratio=4 / 5, is_test=True)
            logger.info("Test post upload completed successfully")
        except Exception as e:
            logger.error(f"Error occurred during test post upload: {str(e)}", exc_info=True)
            raise


    def job_listener(event):
        if event.exception:
            logger.error(f"Job execution failed: {event.job_id}, Exception: {event.exception}")
        else:
            logger.info(f"Job execution succeeded: {event.job_id}")


    scheduler = BlockingScheduler()

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down scheduler...")
        scheduler.shutdown(wait=False)
        sys.exit(0)


    # 왜 안되지??
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill command

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.add_job(lunch_story, "cron", hour=7, id='lunch_story')
    scheduler.add_job(dinner_story, "cron", hour=16, minute=30, id='dinner_story')
    scheduler.add_job(meal_post, "cron", hour=21, id='meal_post')

    logger.info("Scheduler started")
    logger.info("Registered jobs:")
    logger.info("  - Today Lunch story: Daily at 07:00")
    logger.info("  - Today Dinner story: Daily at 16:30")
    logger.info("  - Tomorrow Meal post: Daily at 21:00")
    logger.info("Press Ctrl+C to exit")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")