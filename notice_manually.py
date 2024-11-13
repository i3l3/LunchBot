import os
import requests
import json
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from datetime import datetime
from dotenv import load_dotenv
from instagrapi import Client
from pathlib import Path
from init import init

load_dotenv()

def make_image() -> Image.Image:
    background = (Image.open("assets/background.png")
        .crop((163, 0, 533, 369))
        .resize((1024, 1024))
        .filter(ImageFilter.GaussianBlur(3)))
    draw = ImageDraw.Draw(background, mode="RGBA")
    draw.rectangle(((50, 50), (974, 974)), fill="WHITE")
    return background

def get_lunch(school_info: dict) -> list:
    base_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    args = {
        "KEY": school_info["API_KEY"],                      # API 키
        "Type": "JSON",                                     # 반환값 형식
        "ATPT_OFCDC_SC_CODE": school_info["ofcdc_code"],    # 교육청 코드
        "SD_SCHUL_CODE": school_info["school_code"],        # 학교 코드
        "MMEAL_SC_CODE": school_info["meal_code"],          # 식사 번호 (조식, 중식, 석식, etc...)
        "MLSV_YMD": school_info["date"]                     # 날짜 (YYYYMMDD)
    }
    url = base_url + "?"
    for key, value in args.items():
        url = f"{url}&{key}={value}"
    response = json.loads(requests.get(url).text)
    if datetime(2024, 11, 13) <= datetime.today() < datetime(2024, 11, 15):
        data = "테스트 게시물입니다."
    elif "mealServiceDietInfo" in response:
        data = response["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"].replace("<br/>", "\n")
    else:
        data = "급식 정보가 없습니다."
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    day_name = days[int(datetime.today().strftime("%w"))]
    return [datetime.today().strftime(f"%m월 %d일 {day_name} 급식 정보"), data,
            """- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다.
- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀, 7.고등어, 
  8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산류, 14.호두, 15.닭고기, 
  16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣""",
"- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다."
"\n- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀, 7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, "
"12.토마토, 13.아황산류, 14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣"]

def combine_text(img: Image.Image, lunch: list) -> Image.Image:
    extra_bold = ImageFont.truetype(font="assets/Pretendard-ExtraBold.otf", size=60)
    bold = ImageFont.truetype(font="assets/Pretendard-Bold.otf", size=40)
    bold_small = ImageFont.truetype(font="assets/Pretendard-Bold.otf", size=20)
    draw = ImageDraw.Draw(img)
    draw.text(xy=(100, 100), text=lunch[0], fill=(70,70,70), font=extra_bold)
    draw.text(xy=(100, 280), text=lunch[1], fill=(70,70,70), font=bold)
    draw.text(xy=(100, 924), text=lunch[2], fill=(100,100,100), font=bold_small, anchor="ld")
    return img

def upload_lunch(img: str, lunch: list):
    client = Client()
    client.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
    client.photo_upload(
        Path(img),
        f"{lunch[0]}\n\n{lunch[1]}\n\n{lunch[3]}",
    )

def main():
    init()
    base = make_image()
    lunch = get_lunch({
        "API_KEY": os.getenv("API_KEY"),
        "ofcdc_code": os.getenv("OFCDC_CODE"),
        "school_code": os.getenv("SCHOOL_CODE"),
        "meal_code": os.getenv("MEAL_CODE"),
        "date": datetime.today().strftime("%Y%m%d")
    })
    result = combine_text(base, lunch)
    result.save("assets/result.png")
    upload_lunch("assets/result.png", lunch)


if __name__ == '__main__':
    main()
