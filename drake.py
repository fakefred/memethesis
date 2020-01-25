from PIL import Image, ImageDraw, ImageFont
from textops import make_text
from datetime import datetime
from imageops import vertically_stack

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (400, 250)

# TODO: automate memetheses, with only template image and text spaces provided in csv


def make_drake(drakes, emojis={}, instance='', saveto='drake_output.jpg'):
    dislike_template = Image.open('./res/template/drake/drake_dislike.jpg')
    like_template = Image.open('./res/template/drake/drake_like.jpg')

    drake_panels = []

    for drake in drakes:
        # drake = ('dislike'/'like', text)
        if drake[0] == 'dislike':
            # Image.paste() overwrites Image
            temp = dislike_template.copy()
            text = make_text(
                drake[1], emojis=emojis, box=TEXTSPACE, instance=instance,
                font_path='./res/fonts/NotoSans-Regular.ttf')
            temp.paste(text, box=(370, 12), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'like':
            temp = like_template.copy()
            text = make_text(
                drake[1], emojis=emojis, box=TEXTSPACE, instance=instance,
                font_path='./res/fonts/NotoSans-Regular.ttf')
            temp.paste(text, box=(370, 20), mask=text)
            drake_panels.append(temp)

    meme = vertically_stack(drake_panels)

    meme.save('./output/' + saveto)
    return meme


if __name__ == '__main__':
    make_drake(drakes=[('dislike', "The underground station Rochusplatz on the Cologne Stadtbahn, a light rail system in the German city of Cologne. The station entrance is at the junction of Venloer Straße with Äußere Kanalstraße in the district of Ehrenfeld."),
                       ('dislike', ":cate: :angery:"),
                       ('like', "It was :cate: opened in 1992 and consists of a mezzanine and one island platform with two rail tracks. :angery: The station was previously known as Äußere Kanalstraße, :stonks: but was renamed to its present title on 15 December 2019.")],
               emojis={
        'cate': 'https://cdn.mastodon.technology/custom_emojis/images/000/074/675/original/71593e05a95bd8a7.png',
        'angery': 'https://cdn.mastodon.technology/custom_emojis/images/000/086/057/static/0e9ccdeaf07a28ce.png',
                   'stonks': 'https://cdn.mastodon.technology/custom_emojis/images/000/077/993/static/fa310877bf678f33.png'
    }).show()
