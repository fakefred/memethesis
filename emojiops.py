from PIL import Image
from urllib import request
from os import mkdir, listdir
from re import match, split


def is_in_emoji_form(word: str):
    return bool(match(':\w+:', word))


def smart_split(string: str) -> list:
    return split('\s+|\u200b+', string)


def contains_emojis(content: str, emojis: dict) -> bool:
    # find if any of the words is a custom emoji on the instance
    words = smart_split(content)
    if emojis:  # emojis provided
        for w in words:
            if is_in_emoji_form(w) and w.strip(':') in emojis:
                return True

    return False


def construct_emoji_dict(emoji_list: list) -> dict:
    # emoji_list: [{shortcode: foo, ...}, {shortcode: bar, ...}, ...]
    # return: {foo: ..., bar: ..., ...}
    emoji_dict = {}
    for emoji in emoji_list:
        emoji_dict[emoji['shortcode']] = emoji['static_url']
    return emoji_dict


def combine_filenames(name_from: str, ext_from: str) -> str:
    # combine name_from's name and ext_from's extension
    return (''.join(name_from.split('.')[:-1]) if not name_from.find('.') == -1 else name_from) + '.' + ext_from.split('.')[-1]


def open_in_size(fp: str, size: int):
    # return emoji Image with height of `size`
    orig = Image.open(fp)
    w, h = orig.size
    return orig.resize((w * size // h, size))


def get_emoji(shortcode='', size=24, instance='', emojis={}):
    # takes shortcode, instance the status is from,
    # and emoji dict converted with construct_emoji_dict()
    # returns PIL Image

    # prevent blank; if blank use 'unknown'
    instance = instance if instance else 'unknown'
    # sanitize instance: remove http(s)://
    # used as directory name
    instance = instance.split(
        '/')[2] if match('^https?://', instance) else instance
    path = './res/emojis/' + instance
    try:  # make ./res/emojis/{instance}/ if DNE
        mkdir(path)
    except FileExistsError:
        pass

    for file in listdir(path):
        if file.split('.')[0] == shortcode:
            # emoji on this instance exists
            return open_in_size(path + '/' + file, size)

    # save to ./res/emojis/{instance}/{shortcode}.{extension from emoji url}
    filename = path + '/' + combine_filenames(shortcode, emojis[shortcode])

    try:
        request.urlretrieve(emojis[shortcode], filename)
        return open_in_size(filename, size)
    except request.URLError:
        return Image.open('./res/emojis/error.png').resize((size, size))


def get_emoji_if_is(word: str, size=24, instance='', emojis={}):
    if is_in_emoji_form(word) and word.strip(':') in emojis:
        # is actually an proper emoji
        return get_emoji(shortcode=word.strip(':'), size=size,
                         instance=instance, emojis=emojis)

    return None


if __name__ == '__main__':
    get_emoji(shortcode='cate', instance='https://mastodon.technology', emojis={
              'cate': 'https://cdn.mastodon.technology/custom_emojis/images/000/074/675/original/71593e05a95bd8a7.png'
              }).show()
