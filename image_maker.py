from PIL import Image, ImageFilter, ImageDraw, ImageFont


def get_offset(ratio: float, w, h):
    # 목표 비율에 맞춰 중앙 크롭 영역 계산
    current_ratio = w / h

    if current_ratio > ratio:
        # 이미지가 목표보다 더 넓음 -> 좌우를 잘라야 함
        new_width = int(h * ratio)
        offset = (w - new_width) / 2
        left = offset
        upper = 0
        right = w - offset
        lower = h
    else:
        # 이미지가 목표보다 더 높음 -> 상하를 잘라야 함
        new_height = int(w / ratio)
        offset = (h - new_height) / 2
        left = 0
        upper = offset
        right = w
        lower = h - offset

    return left, upper, right, lower


def crop_img(img: Image, ratio: float) -> Image:
    original_width, original_height = img.size
    left, upper, right, lower = get_offset(ratio, original_width, original_height)

    cropped_img = img.crop((left, upper, right, lower))
    cropped_width, cropped_height = cropped_img.size
    new_width = 1080
    new_height = int(cropped_height * (1080 / cropped_width))

    return cropped_img.resize((new_width, new_height), Image.Resampling.LANCZOS)


def write_text(img: Image, offset: int, ratio: float, title: str, main: str, bottom: str):
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # offset을 뺀 영역에서 목표 비율에 맞는 사각형 계산
    inner_w = w - 2 * offset
    inner_h = h - 2 * offset

    left, upper, right, lower = get_offset(ratio, inner_w, inner_h)

    # offset을 더해서 실제 좌표로 변환
    rect_left = left + offset
    rect_upper = upper + offset
    rect_right = right + offset
    rect_lower = lower + offset

    draw.rectangle([(rect_left, rect_upper), (rect_right, rect_lower)], fill="white")

    font = "assets/PretendardVariable.ttf"

    title_font = ImageFont.truetype(font, 65)
    title_font.set_variation_by_name("ExtraBold")
    draw.text((80 + rect_left, 80 + rect_upper), title, font=title_font, fill=(70, 70, 70))

    main_font = ImageFont.truetype(font, 60)
    main_font.set_variation_by_name("SemiBold")
    draw.text((80 + rect_left, 300 + rect_upper), main, font=main_font, fill=(70, 70, 70))

    bottom_font = ImageFont.truetype(font, 25)
    bottom_font.set_variation_by_name("Light")
    draw.text((80 + rect_left, rect_lower - 80), bottom, font=bottom_font, fill=(100, 100, 100), anchor="ld")

    return img


if __name__ == "__main__":
    offset = 50
    bg = "assets/boram1.png"
    title = "8월 22일 금요일 급식 정보"
    main = ("차수수밥\n"
           "유부장국\n"
           "묵은지김치찜\n"
           "오리훈제/머스터드소스.+무쌈\n"
           "오이부추무침\n"
           "배추김치\n"
           "제주청귤주스")
    bottom = ("- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다.\n"
             "- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀,\n"
             "   7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산류,\n"
             "   14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣\n"
             "- 알레르기 정보는 게시글 설명란에 있습니다.")

    post_ratio = 4 / 5
    post_bg = crop_img(Image.open(bg), post_ratio).filter(ImageFilter.GaussianBlur(3))
    post_bg = write_text(post_bg, offset, post_ratio, title, main, bottom)
    post_bg.save("assets/post.jpg")

    story_ratio = 9 / 16
    story_bg = crop_img(Image.open(bg), story_ratio).filter(ImageFilter.GaussianBlur(3))
    story_bg = write_text(story_bg, offset, story_ratio, title, main, bottom)
    story_bg.save("assets/story.jpg")