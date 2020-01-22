from PIL import Image, ImageDraw, ImageFont
from textops import fit_text_in_box, fit_text_with_emojis_in_box
from datetime import datetime

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (400, 250)

# TODO: automate memetheses, with only template image and text spaces provided in csv


def make_drake(dislike='', like='', emojis={}, instance='', saveto='drake_output.jpg'):
    template = Image.open('./res/template/drake.jpg')

    dislike_text = fit_text_in_box(
        dislike, emojis=emojis, box=TEXTSPACE, 
        instance=instance, font_path='./res/fonts/NotoSans-Regular.ttf')

    like_text = fit_text_in_box(
        like, emojis=emojis, box=TEXTSPACE, 
        instance=instance, font_path='./res/fonts/NotoSans-Regular.ttf')

    template.paste(dislike_text, box=(
        370, 20), mask=dislike_text)
    template.paste(like_text, box=(
        370, 285), mask=like_text)

    template.save('./output/' + saveto)
    return template


if __name__ == '__main__':
    make_drake(dislike="The underground station Rochusplatz on the Cologne Stadtbahn, a light rail system in the German city of Cologne. The station entrance is at the junction of Venloer Straße with Äußere Kanalstraße in the district of Ehrenfeld.",
               like="It was :cate: opened in 1992 and consists of a mezzanine and one island platform with two rail tracks. :angery: The station was previously known as Äußere Kanalstraße, :stonks: but was renamed to its present title on 15 December 2019.",
               emojis={
                   'cate': 'https://cdn.mastodon.technology/custom_emojis/images/000/074/675/original/71593e05a95bd8a7.png',
                   'angery': 'https://cdn.mastodon.technology/custom_emojis/images/000/086/057/static/0e9ccdeaf07a28ce.png',
                   'stonks': 'https://cdn.mastodon.technology/custom_emojis/images/000/077/993/static/fa310877bf678f33.png'
               }).show()
