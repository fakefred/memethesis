from PIL import Image
from textops import make_text
import re

def parse_caption(line: str) -> str:
    if (line.lower().startswith('caption:') and
              line.lower().replace('caption:', '', 1).strip()):
        # is in a caption pattern
        return re.sub('^caption:', '', line, flags=re.I)
    return None

def make_caption(text='', emojis={}, instance='', width=800,
                 font='./res/fonts/NotoSans-Regular.ttf'):
    caption = Image.new('RGBA', (width, 120), color=(255, 255, 255, 255))
    cap_text = make_text(text, box=(width - 20, 100), font_path=font,
                        init_font_size=64, emojis=emojis)
    caption.paste(cap_text, box=(10, 10), mask=cap_text)
    return caption
