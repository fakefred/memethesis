from PIL import Image, ImageDraw, ImageFont
from caption import parse_caption, make_caption
from separator import is_sep, make_sep
from textops import make_text
from imageops import stack
from re import match

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACES = [(380, 250),  # these brain size
              (380, 250),  # panels have
              (380, 240),  # various heights
              (380, 255),
              (380, 250)]


def parse_brainsize(content: str):
    lines = content.splitlines()
    brains = []  # tuples of (dislike/like, text)
    is_brainsize = False

    for line in lines:
        # remove zero-width spaces and leading/trailing whitespace
        naked_line = line.replace('\u200b', '').strip()
        m = match('^:brain[1-5]: ', naked_line)
        # returns None when not found, else substring ':brainx:'
        if m is not None:
            # :brain|x|:
            # 012345|6|7
            brainsize = int(m.group(0)[6])  # guaranteed to be within [1-5]
            brains.append((brainsize, naked_line.replace(
                f':brain{brainsize}:', '', 1).strip()))
            is_brainsize = True

        elif parse_caption(naked_line):
            brains.append((
                'caption',
                parse_caption(naked_line)
            ))

        elif is_sep(naked_line):
            brains.append(('sep', ''))
        

    if is_brainsize:
        return brains

    return None


def make_brainsize(brains: list, emojis={}, font='./res/fonts/NotoSans-Regular.ttf',
                   instance='', saveto='brain_output.jpg'):
    templates = [Image.open(
        f'./res/template/brainsize/brain{n}.jpg') for n in (1, 2, 3, 4, 5)]
    # templates[n] = meme template panel for brain size n+1

    brain_panels = []

    for brain in brains:
        # brain = ([1-5], text)
        if brain[0] in range(1, 6):
            temp = templates[brain[0] - 1].copy()
            text = make_text(
                brain[1], emojis=emojis, box=TEXTSPACES[brain[0] - 1],
                instance=instance, font_path=font)
            temp.paste(text, box=(10, 8), mask=text)
            brain_panels.append(temp)
        elif brain[0] == 'caption':
            brain_panels.append(
                make_caption(text=brain[1], emojis=emojis,
                             instance=instance, width=800, font=font)
            )
        elif brain[0] == 'sep':
            brain_panels.append(make_sep(width=800))

    meme = vertically_stack(brain_panels)

    meme.save('./output/' + saveto)
    return meme


if __name__ == '__main__':
    make_brainsize(brains=[(1, "The underground station Rochusplatz on the Cologne Stadtbahn, a light rail system in the German city of Cologne. The station entrance is at the junction of Venloer Straße with Äußere Kanalstraße in the district of Ehrenfeld."),
                           (2, ":cate: :angery:"),
                           (3, "It was :cate: opened in 1992 and consists of a mezzanine and one island platform with two rail tracks."),
                           (4, ":angery: The station was previously known as Äußere Kanalstraße,"),
                           (5, ":stonks: but was renamed to its present title on 15 December 2019.")],
                   emojis={
        'cate': 'https://cdn.mastodon.technology/custom_emojis/images/000/074/675/original/71593e05a95bd8a7.png',
        'angery': 'https://cdn.mastodon.technology/custom_emojis/images/000/086/057/static/0e9ccdeaf07a28ce.png',
        'stonks': 'https://cdn.mastodon.technology/custom_emojis/images/000/077/993/static/fa310877bf678f33.png'
    }).show()
