from PIL import Image, ImageDraw, ImageFont
from textops import fit_text_in_box
from datetime import datetime

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (400, 250)

# TODO: automate memetheses, with only template image and text spaces provided in csv


def make_drake(dislike='', like='', saveto='drake_output.jpg'):
    template = Image.open('./res/template/drake.jpg')
    IMSIZE = template.size

    dislike_text = fit_text_in_box(
        dislike, box=TEXTSPACE, font_path='./res/fonts/NotoSansCJKsc_Regular.otf')

    like_text = fit_text_in_box(
        like, box=TEXTSPACE, font_path='./res/fonts/NotoSansCJKsc_Regular.otf')

    template.paste(dislike_text, box=(
        370, 20), mask=dislike_text)
    template.paste(like_text, box=(
        370, IMSIZE[1] // 2 + 20), mask=like_text)

    template.save('./output/' + saveto)
