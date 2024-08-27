from dotenv import load_dotenv
import os
import time
import locale
import requests

load_dotenv()
locale.setlocale(locale.LC_TIME, "ko_KR")

params = {
    "Type": "json",
    "KEY": os.environ.get("API_KEY"),
    "ATPT_OFCDC_SC_CODE": os.environ.get("OFFICE_OF_EDU_CODE"),
    "SD_SCHUL_CODE": os.environ.get("SCHOOL_CODE"),
    "MMEAL_SC_CODE": "2",
    "MLSV_YMD": time.strftime("%Y%m%d"),
}
baseURL = "https://open.neis.go.kr/hub/mealServiceDietInfo"

desc = ("- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다.\n"
        "- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀, 7.고등어, 8.게, 9.새우, 10.돼지고기, "
        "11.복숭아, 12.토마토, 13.아황산류, 14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣")


def get_lunch() -> str:
    response = requests.get(baseURL, params=params)
    jsonData: dict = response.json()
    if "mealServiceDietInfo" in jsonData:
        meal: str = jsonData["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
    else:
        meal: str = "급식 정보가 존재하지 않습니다."
    meal = meal.replace("<br/>", "\n")
    return meal


def get_desc() -> str:
    return desc


if __name__ == '__main__':
    print(time.strftime("%Y년 %m월 %d일 %a요일 급식 알림\n"))
    print(get_lunch())
    print("\n" + get_desc())
