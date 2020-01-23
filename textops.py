from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from emojiops import get_emoji_if_is, smart_split, contains_emojis
from re import sub


def replace_emojo(string: str,  repl: str) -> str:
    # criteria:
    # before[whitespace]:text_without_whitespace:[whitespace]after
    return sub('\s:\S+:\s', repl, string)


def wrap_text(text: str, maxwidth: int, font) -> str:
    # maxwidth: in pixels
    # TODO: hyphenation

    # initiate drawing context
    canvas = Image.new('RGB', (1, 1), color=(255, 255, 255))
    draw = Draw(canvas)

    # split words and iterate
    words = text.split(' ')
    current_line = ''
    wrapped_text = ''
    for word in words:
        line_width = draw.textsize(current_line + word, font=font)[0]
        if line_width <= maxwidth:
            # append word
            current_line += word + ' '
            wrapped_text += word + ' '
        else:
            # linebreak
            wrapped_text += '\n' + word + ' '
            # reset buffer
            current_line = word + ' '

    return wrapped_text


def fit_text_in_box(text: str, box=(0, 0), font_path='',
                    color=(0, 0, 0, 255), emojis={}, instance=''):
    if contains_emojis(text, emojis):
        # fancy rendering enabled
        # redirect to fit_text_with_emojis_in_box()
        return fit_text_with_emojis_in_box(
            text, emojis=emojis, instance=instance,
            box=box, font_path=font_path, color=color)

    canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))
    draw = Draw(canvas)
    textsize = (box[0] + 1, box[1] + 1)
    font_size = 76  # max font size is 72; decrease by 4 until fit
    while textsize[0] > box[0] or textsize[1] > box[1]:  # doesn't fit
        font_size -= (4 if font_size > 32 else 2)
        font = truetype(font_path, size=font_size)
        # try to fit in the horizontal boundary
        wrapped = wrap_text(text, box[0], font)
        textsize = draw.multiline_textsize(wrapped, font=font)
        # when wrapped text fits in box, loop will exit, and font is remembered

    draw.multiline_text((0, 0), wrapped, fill=color, font=font)
    return canvas


def fit_text_with_emojis_in_box(text: str, emojis={}, instance='', box=(0, 0),
                                font_path='', color=(0, 0, 0, 255)):
    # different method
    # used for text with custom emojis
    # less efficient than without
    # TODO: flag for no-render-emoji
    # split text into individual words, then draw them sequentially.
    words = smart_split(text)
    canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))  # method scope

    x, y = 0, 0
    font_size = 76

    while True:
        # (re-)initiate canvas
        canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))
        draw = Draw(canvas)

        # for each font size, first fill the width.
        # if the height exceeds the size of the box, reduce font size.
        # repeat font size reduction until fits.
        if 0 < font_size < 32:
            font_size -= 2
        elif font_size >= 32:
            font_size -= 4
        else:
            break

        font = truetype(font_path, size=font_size)
        space_width = draw.textsize(' ', font=font)[0]
        line_height = int(font_size * 1.2)

        # start filling words
        idx = 0  # position in list `words`
        y = 0
        while idx < len(words):  # words not depleted
            # new line
            x = 0
            word = words[idx]

            emoji = get_emoji_if_is(
                word, size=font_size, instance=instance, emojis=emojis)
            # emoji: Image of it if is an emoji, else None
            if emoji:
                next_word_width = emoji.size[0]
            else:
                next_word_width = draw.textsize(word, font=font)[0]

            # skip this size if even a single word won't fit
            if next_word_width > box[0]:
                break

            # fill line until it would overflow
            while x + next_word_width <= box[0]:
                word = words[idx]
                emoji = get_emoji_if_is(word, size=font_size,
                                        instance=instance, emojis=emojis)
                word_width = (emoji.size[0]
                              if emoji
                              else draw.textsize(word, font=font)[0])

                if emoji:
                    if 'A' in emoji.getbands():
                        # emoji has Alpha channel, aka transparency
                        canvas.paste(emoji, box=(x, y), mask=emoji)
                    else:
                        canvas.paste(emoji, box=(x, y))
                else:
                    draw.text((x, y - font_size // 10), word, fill=color, font=font)

                x += word_width + space_width
                idx += 1
                if idx >= len(words):
                    break
                next_word_width = draw.textsize(words[idx], font=font)[0]

            y += line_height

        if y <= box[1] and idx == len(words):
            return canvas
