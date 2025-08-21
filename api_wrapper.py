import json
import urllib
import requests
import os

def get_meals(date: str):
    api_key = os.getenv("API_KEY")
    ofcdc = os.getenv("OFCDC_CODE")
    school = os.getenv("SCHOOL_CODE")

    base_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    args = {
        "KEY": api_key,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": ofcdc,
        "SD_SCHUL_CODE": school,
        "MLSV_YMD": date,
    }
    url = base_url + "?" + urllib.parse.urlencode(args)
    response = requests.get(url)
    return json.loads(response.text)["mealServiceDietInfo"][1]["row"]

if __name__ == "__main__":
    from dotenv import load_dotenv
    import pprint

    load_dotenv()
    pprint.pprint(get_meals("20250821"))
