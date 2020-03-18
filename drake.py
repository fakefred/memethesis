from PIL import Image, ImageDraw, ImageFont
from caption import parse_caption, make_caption
from separator import is_sep, make_sep
from textops import make_text
from imageops import stack
import re

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (400, 250)

# TODO: automate memetheses, with only template image and text spaces provided in csv


def parse_drake(content: str):
    lines = content.splitlines()
    drakes = []  # tuples of (dislike/like, text)
    is_drake = False

    description = '(Drake meme) '

    for line in lines:
        # remove zero-width spaces and leading/trailing whitespace
        naked_line = line.replace('\u200b', '').strip()
        # :drake_dislike: some text after it, not none [yes]
        # :drake_dislike: [no]
        if (naked_line.startswith(':drake_dislike: ') and
                naked_line.replace(':drake_dislike: ', '', 1).strip()):
            drakes.append((
                'dislike',
                # remove leftmost :drake_dislike:
                naked_line.replace(':drake_dislike: ', '', 1).strip()))
            description += 'dislikes "{0}"; '.format(drakes[-1][1])
            is_drake = True

        elif (naked_line.startswith(':drake_like: ') and
                naked_line.replace(':drake_like: ', '', 1).strip()):
            drakes.append((
                'like',
                naked_line.replace(':drake_like: ', '', 1).strip()))
            description += 'likes "{0}"; '.format(drakes[-1][1])
            is_drake = True

        elif parse_caption(naked_line) is not None:
            drakes.append((
                'caption',
                parse_caption(naked_line)
            ))
            description += 'caption "{0}"; '.format(drakes[-1][1])

        elif is_sep(naked_line):
            drakes.append(('sep', ''))

    if is_drake:
        return (drakes, description[:-2])

    return (None, None)


def make_drake(drakes: list, emojis={}, font='./res/fonts/NotoSans-Regular.ttf',
               instance='', saveto='drake_output.jpg', stroke=False):
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
                font_path=font, stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 12), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'like':
            temp = like_template.copy()
            text = make_text(
                drake[1], emojis=emojis, box=TEXTSPACE, instance=instance,
                font_path=font, stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 20), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'caption':
            drake_panels.append(
                make_caption(text=drake[1], emojis=emojis,
                             instance=instance, width=800, font=font,
                             stroke=stroke)
            )
        
        elif drake[0] == 'sep':
            drake_panels.append(make_sep(width=800))

    meme = stack(drake_panels)

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
