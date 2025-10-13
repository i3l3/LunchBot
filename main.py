from dotenv import load_dotenv
from datetime import date
from PIL import Image, ImageFilter
from locale import setlocale
from api_wrapper import get_meals, upload_post, upload_story
from image_maker import crop_img, write_text
import locale
import os

setlocale(locale.LC_TIME, "ko_KR")
load_dotenv()
meal_name = ["조식", "중식", "석식"]

bottom = ("- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다.\n"
        "- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀,\n"
        "   7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산류,\n"
        "   14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣\n"
        "- 알레르기 정보는 게시글 설명란에 있습니다.")

def upload(code: int, offset: int, bg: str, ratio=4/5, is_post=True, is_test=False):
    # code: 조식, 중식, 석식 불러오기
    # 1: 조식 2: 중식 3: 석식
    if is_test:
        post_bg = crop_img(Image.open(bg), ratio).filter(ImageFilter.GaussianBlur(3))
        post_bg = write_text(post_bg, offset, ratio, "테스트 게시물", "테스트 게시물입니다.", bottom)
        post_bg.save("assets/post.png")

        if is_post:
            upload_post("assets/post.png", "테스트 게시물입니다.")
        elif not is_post:
            upload_story("assets/post.png")
        os.remove("assets/post.png")
        return

    meals = get_meals(date.today().strftime("%Y%m%d"))
    for meal in meals:
        if meal["MMEAL_SC_CODE"] == str(code):
            title = date.today().strftime(f"%m월 %d일 %A {meal_name[code - 1]} 정보")
            main = meals[0]["DDISH_NM"].replace("<br/>", "\n")

            post_bg = crop_img(Image.open(bg), ratio).filter(ImageFilter.GaussianBlur(3))
            post_bg = write_text(post_bg, offset, ratio, title, main, bottom)
            post_bg.save("assets/post.png")

            # webhook logging?
            if is_post:
                upload_post("assets/post.png", f"{title}\n\n{main}\n\n{bottom}")
            elif not is_post:
                upload_story("assets/post.png")
            os.remove("assets/post.png")

if __name__ == "__main__":
    upload(2, 50, "assets/boram1.png", 4/5, is_test=True)
    upload(2, 50, "assets/boram1.png", 9/16, is_post=False, is_test=True)
