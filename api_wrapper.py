import json
import logging
import urllib
import requests
import os
from instagrapi import Client
from instagrapi.types import Usertag
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

def upload_post(locations: list, description: str):
    logger = logging.getLogger(__name__)

    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    author = os.getenv("INSTAGRAM_AUTHOR")

    client = Client()
    if os.path.exists("session.json"):
        client.load_settings("session.json")
        client.login(username, password)
    else:
        client.login(username, password)
        client.dump_settings("session.json")

    extra_data = {}
    usertags = []
    if author:
        users = client.search_following(str(client.user_id), author)
        if len(users) > 0:
            usertags.append(Usertag(user=users[0], x=0.5, y=0.5))
            extra_data["invite_coauthor_user_id"] = users[0].pk
        else:
            logger.info(f"User @{author} not found")



    if len(locations) == 1:
        client.photo_upload(locations[0], description, extra_data=extra_data)
    else:
        client.album_upload([Path(location) for location in locations], description,
                            usertags=usertags, extra_data=extra_data)

def upload_story(location: str):
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    client = Client()
    if os.path.exists("session.json"):
        client.load_settings("session.json")
        client.login(username, password)
    else:
        client.login(username, password)
        client.dump_settings("session.json")
    client.photo_upload_to_story(Path(location))

if __name__ == "__main__":
    from dotenv import load_dotenv
    import pprint

    load_dotenv()
    pprint.pprint(get_meals("20250821"))
