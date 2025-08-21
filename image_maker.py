from PIL import Image, ImageFilter, ImageDraw, ImageFont


def crop_img(img: Image, ratio: float) -> Image:
    original_width, original_height = img.size
    if original_width / original_height > ratio:
        new_width = int(original_height * ratio)
        offset = (original_width - new_width) / 2
        left = offset
        upper = 0
        right = original_width - offset
        lower = original_height
    else:
        new_height = int(original_width / ratio)
        offset = (original_height - new_height) / 2
        left = 0
        upper = offset
        right = original_width
        lower = original_height - offset

    cropped_img = img.crop((left, upper, right, lower))
    cropped_width, cropped_height = cropped_img.size
    new_width = 1080
    new_height = int(cropped_height * (1080 / cropped_width))

    return cropped_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def write_text(img: Image, offset: int, title: str, main: str, bottom: str):
    draw = ImageDraw.Draw(img)
    w, h = bg.size
    draw.rectangle([(offset, offset), (w - offset, h - offset)], fill="white")

    font = "assets/PretendardVariable.ttf"
    title_font = ImageFont.truetype(font, 65)
    title_font.set_variation_by_name("ExtraBold")
    draw.text((80 + offset, 80 + offset), title, font=title_font, fill=(70, 70, 70))
    main_font = ImageFont.truetype(font, 60)
    main_font.set_variation_by_name("SemiBold")
    draw.text((80 + offset, 300 + offset), main, font=main_font, fill=(70, 70, 70))
    bottom_font = ImageFont.truetype(font, 25)
    bottom_font.set_variation_by_name("Light")
    draw.text((80 + offset, h - 80 - offset), bottom, font=bottom_font, fill=(100, 100, 100), anchor="ld")
    return img


if __name__ == "__main__":
    offset = 50
    bg = crop_img(Image.open("assets/boram1.png"), 4 / 5).filter(ImageFilter.GaussianBlur(3))
    bg = write_text(bg, offset,
                    "8월 22일 금요일 급식 정보",
                    "차수수밥\n"
                    "유부장국\n"
                    "묵은지김치찜\n"
                    "오리훈제/머스터드소스.+무쌈\n"
                    "오이부추무침\n"
                    "배추김치\n"
                    "제주청귤주스",
                    "- 요리명에 표시된 번호 : 알레르기를 유발할수 있는 식재료입니다.\n"
                    "- 알레르기 유발 식재료 번호 : 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀,\n"
                    "   7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산류,\n"
                    "   14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴, 전복, 홍합 포함), 19.잣\n"
                    "- 알레르기 정보는 게시글 설명란에 있습니다.")
    bg.show()
    bg.save("assets/boram3.png")
