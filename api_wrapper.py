import json
import urllib
import requests
import os
from instagrapi import Client
from pathlib import Path

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

def get_times(date: str):
    api_key = os.getenv("API_KEY")
    ofcdc = os.getenv("OFCDC_CODE")
    school = os.getenv("SCHOOL_CODE")

    base_url = "https://open.neis.go.kr/hub/hisTimetable"
    args = {
        "KEY": api_key,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": ofcdc,
        "SD_SCHUL_CODE": school,
        "ALL_TI_YMD": date,
    }
    url = base_url + "?" + urllib.parse.urlencode(args)
    response = requests.get(url)
    return json.loads(response.text)["hisTimetable"][1]["row"]

def upload_post(location: str, description: str):
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    author = os.getenv("INSTAGRAM_AUTHOR")
    extra_data = {}
    if author:
        extra_data["invite_coauthor_user_id"] = author
    client = Client()
    client.login(username, password)
    client.photo_upload(Path(location), description, extra_data=extra_data)

def upload_story(location: str):
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    client = Client()
    client.login(username, password)
    client.photo_upload_to_story(Path(location))

if __name__ == "__main__":
    from dotenv import load_dotenv
    import pprint

    load_dotenv()
    pprint.pprint(get_meals("20250821"))
    # pprint.pprint(get_times("20251013"))
