from PIL import Image, ImageDraw
from emojiops import is_in_emoji_form, get_emoji
from args import parse_arguments
import pysnooper

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

HEAD = (55, 36)
BODY = (8, 227)


def parse_stonks(content: str):
    lines = content.splitlines()
    args = parse_arguments(content)

    stonks = {
        'head': '',
        'flip': args['flip']  # horizontal flip
        # TODO: customize text
    }

    for line in lines:
        # remove zero-width spaces and leading/trailing whitespace
        naked_line = line.replace('\u200b', '').strip()
        if (naked_line.startswith(':stonks: ') and
                naked_line.replace(':stonks: ', '', 1).strip()):
            words = naked_line.replace(':stonks: ', '', 1).split()
            if words and is_in_emoji_form(words[0]):
                stonks['head'] = words[0].strip(':')
                return stonks

    return None


def make_stonks(stonks: dict, emojis={}, font='./res/fonts/NotoSans-Regular.ttf',
                instance='', saveto='stonks_output.jpg'):
    stonks_template = Image.open('./res/template/stonks/bg_stonks.jpg')
    mememan = Image.open('./res/template/stonks/headless_mememan.png')

    emoji = get_emoji(shortcode=stonks['head'], size=220,
                      instance=instance, emojis=emojis)

    if stonks['flip']:
        emoji = emoji.transpose(method=Image.FLIP_LEFT_RIGHT)

    stonks_template.paste(emoji, box=HEAD,
                          mask=emoji if 'A' in emoji.getbands() else None)
    stonks_template.paste(mememan, box=BODY, mask=mememan)

    stonks_template.save('./output/' + saveto)
    return stonks_template


if __name__ == '__main__':
    make_stonks({'head': 'catto', 'flip': True}, emojis={
        'catto': 'https://cdn.mastodon.technology/custom_emojis/images/000/082/698/original/0ed6bafb0cbb3008.png'
    }, instance='https://mastodon.technology').show()
