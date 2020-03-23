from re import sub, match
from drake import parse_drake, make_drake
from brainsize import parse_brainsize, make_brainsize
from stonks import parse_stonks, make_stonks
from woman_yelling import parse_woman_yelling, make_woman_yelling
from emojiops import construct_emoji_dict
from fontconfig import LANGS, MONO, FONTS
from args import parse_arguments
from html import unescape
from htmlops import TootParser


def uncurse(toot: str):
    # toots come in a cursed format (HTML)
    # tags like <p>, <a href=""> and <br /> may appear
    parser = TootParser()
    parser.feed(toot)
    blessed = parser.content

    # also parse HTML encoding
    return unescape(blessed)


def prepare(toot: str, emojis={}, instance='', saveto='') -> tuple:
    # return meme type and parsed info if toot is meme
    # else, return 'not a meme' and None.
    blessed = uncurse(toot)
    if not blessed.strip():
        return ('empty', None, None)

    arguments = parse_arguments(blessed)

    # overall priority:
    # font > mono > lang
    # arguments here are filled with default values in args.py
    # mono overrides lang (if mono is present, the elif will not be entered)
    if arguments['mono']:
        font = MONO
    elif arguments['lang'] in LANGS:
        font = LANGS[arguments['lang']]
    else:
        return ('language not supported', None, None)

    stroke = False
    if arguments['font'] in FONTS:
        # font overrides mono and lang
        font = FONTS[arguments['font']]
        if arguments['font'] == 'impact':
            stroke = True  # render text in its stroke (outline)
    elif arguments['font'] == 'unchanged':
        # default value in args.py
        pass
    else:
        return ('font not supported', None, None)


    drakes, desc = parse_drake(blessed)
    if drakes:
        # is drake meme (or at least a portion thereof)
        return ('Drake', {
            'drakes': drakes,
            'emojis': emojis,
            'font': font,
            'stroke': stroke,
            'instance': instance,
            'saveto': saveto
        }, desc)  # return meme type and parsed info

    # uh oh, is not drake
    brains, desc = parse_brainsize(blessed)
    if brains:
        # is brain size meme
        return ('Brain Size', {
            'brains': brains,
            'emojis': emojis,
            'font': font,
            'stroke': stroke,
            'instance': instance,
            'saveto': saveto
        }, desc)

    stonks, desc = parse_stonks(blessed)
    if stonks:
        # is stonks meme
        return ('Stonks', {
            'stonks': stonks,
            'emojis': emojis,
            'font': font,
            'stroke': stroke,
            'instance': instance,
            'saveto': saveto
        }, desc)

    woman_yelling, desc = parse_woman_yelling(blessed)
    if woman_yelling:
        # is woman yelling meme
        return ('Woman Yelling', {
            'entities': woman_yelling,
            'emojis': emojis,
            'font': font,
            'stroke': stroke,
            'instance': instance,
            'saveto': saveto
        }, desc)
    # NOTE TO SELF: do not forget to add proxy to def memethesis()
    # when adding a new meme type
    return ('not a meme', None, None)


def memethesis(fmt: str, info: dict):
    # takes format and info
    # calls corresponding memethesizing function
    if fmt == 'Drake':
        meme = make_drake(**info)
    elif fmt == 'Brain Size':
        meme = make_brainsize(**info)
    elif fmt == 'Stonks':
        meme = make_stonks(**info)
    elif fmt == 'Woman Yelling':
        meme = make_woman_yelling(**info)

    return meme


if __name__ == '__main__':
    pass
