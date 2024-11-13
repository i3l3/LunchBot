import os
import requests
from os import path
from dotenv import load_dotenv

load_dotenv()

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
def init():
    background_url = os.getenv("BACKGROUND_URL")
    bold_font_url = os.getenv("BOLD_FONT_URL")
    extra_bold_font_url = os.getenv("EXTRA_BOLD_FONT_URL")

    if not path.exists("assets"):
        os.mkdir("assets")
    if not path.exists("assets/background.png") and background_url != "":
        download(background_url, "assets/background.png")
        print(f"Downloading background.png in {os.getcwd()}/assets/background.png")
    if not path.exists("assets/Pretendard-Bold.otf") and bold_font_url != "":
        download(bold_font_url, "assets/Pretendard-Bold.otf")
        print(f"Downloading background.png in {os.getcwd()}/assets/Pretendard-Bold.otf")
    if not path.exists("assets/Pretendard-ExtraBold.otf") and extra_bold_font_url != "":
        download(extra_bold_font_url, "assets/Pretendard-ExtraBold.otf")
        print(f"Downloading background.png in {os.getcwd()}/assets/Pretendard-ExtraBold.otf")

if __name__ == "__main__":
    init()
