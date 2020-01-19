from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
import re


def replace_emojo(string: str,  repl: str) -> str:
    # criteria:
    # before[whitespace]:text_without_whitespace:[whitespace]after
    return re.sub('\s:\S+:\s', repl, string)


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


def fit_text_in_box(text: str, box=(0, 0), font_path='', color=(0, 0, 0, 255), emojo=True):
    canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))
    draw = Draw(canvas)
    textsize = (box[0] + 1, box[1] + 1)
    fontsize = 76  # max font size is 72; decrease by 4 until fit
    while textsize[0] > box[0] or textsize[1] > box[1]:  # doesn't fit
        fontsize -= 4
        font = truetype(font_path, size=fontsize)
        # TODO: draw emojo
        # try to fit in the horizontal boundary
        wrapped = wrap_text(text, box[0], font)
        textsize = draw.multiline_textsize(wrapped, font=font)
        # when wrapped text fits in box, loop will exit, and font is remembered

    draw.multiline_text((0, 0), wrapped, fill=color, font=font)
    return canvas
