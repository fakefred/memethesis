from PIL import Image, ImageDraw
from emojiops import is_in_emoji_form, get_emoji
from textops import make_text
from args import parse_arguments

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

HEAD = (55, 36)
BODY = (8, 227)
TEXT = (490, 350)


def parse_stonks(content: str):
    # stonks and stinks (aka badstonks)
    lines = content.splitlines()
    args = parse_arguments(content)

    stonks = {
        'head': '',
        'flip': args['flip'],  # horizontal flip
        'bad': False,
        'custom_text': ''
    }

    for line in lines:
        # remove zero-width spaces and leading/trailing whitespace
        naked_line = line.replace('\u200b', '').strip()
        for idx, emj in enumerate([':stonks: ', ':badstonks: ']):
            if (naked_line.startswith(emj) and
                    naked_line.replace(emj, '', 1).strip()):
                words = naked_line.replace(emj, '', 1).split()
                if words and is_in_emoji_form(words[0]):
                    stonks['head'] = words[0].strip(':')
                    stonks['bad'] = True if idx == 1 else False
                    if len(words) > 1:
                        # custom text present
                        stonks['custom_text'] = ' '.join(words[1:])
                    return stonks
    return None


def make_stonks(stonks: dict, emojis={}, font='./res/fonts/NotoSans-Regular.ttf',
                instance='', saveto='stonks_output.jpg'):
    if stonks['bad'] and stonks['custom_text']:
        stonks_template = Image.open(
            './res/template/stonks/bg_stinks_notext.jpg')
    elif stonks['bad'] and not stonks['custom_text']:
        stonks_template = Image.open('./res/template/stonks/bg_stinks.jpg')
    elif not stonks['bad'] and stonks['custom_text']:
        stonks_template = Image.open(
            './res/template/stonks/bg_stonks_notext.jpg')
    elif not stonks['bad'] and not stonks['custom_text']:
        stonks_template = Image.open('./res/template/stonks/bg_stonks.jpg')

    mememan = Image.open('./res/template/stonks/headless_mememan.png')

    emoji = get_emoji(shortcode=stonks['head'], size=220,
                      instance=instance, emojis=emojis)

    if stonks['flip']:
        emoji = emoji.transpose(method=Image.FLIP_LEFT_RIGHT)

    stonks_template.paste(emoji, box=HEAD,
                          mask=emoji if 'A' in emoji.getbands() else None)
    stonks_template.paste(mememan, box=BODY, mask=mememan)

    if stonks['custom_text']:
        text = make_text(stonks['custom_text'], box=(290, 95), font_path=font,
                         color=WHITE, stroke=BLACK, emojis=emojis, instance=instance)
        stonks_template.paste(text, box=TEXT, mask=text)

    stonks_template.save('./output/' + saveto)
    return stonks_template


if __name__ == '__main__':
    make_stonks({'head': 'catto', 'flip': True, 'bad': False}, emojis={
        'catto': 'https://cdn.mastodon.technology/custom_emojis/images/000/082/698/original/0ed6bafb0cbb3008.png'
    }, instance='https://mastodon.technology').show()
