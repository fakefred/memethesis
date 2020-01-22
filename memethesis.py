from re import sub
from drake import make_drake

# Test toots
TOOTS = ['<p>stole some emotes from .social while they werent lookin</p><p>:birdsite: :angery: :breathe: :gnomed: :dab: :thaenkin: :thinkhappy: :tinking:</p>',
         '<p>drake + <br />:drake_dislike: dislike<br />:drake_like: desliek<br /><a href="https://mastodon.technology/tags/tag" class="mention hashtag" rel="tag">#<span>tag</span></a></p>',
         ':drake_dislike: Cable News Network <br /> :drake_like: Convolutionary Neural Network',
         '<p><span class="h-card"><a href="https://botsin.space/@memethesis" class="u-url mention" rel="nofollow noopener" target="_blank">@<span>memethesis</span></a></span>:drake_dislike: Run bot on proper server<br>:drake_like: Run bot on VS Code</p>',
         '<p><span class="h-card"><a href="https://botsin.space/@memethesis" class="u-url mention">@<span>memethesis</span></a></span> :drake_dislike: Having enough prudence not to have the bot run unattended in its alpha phase</p><p>:drake_like: Running the bot overnight in gnu screen while I go to sleep</p>',
         '<p><span class=\"h-card\"><a href=\"https://botsin.space/@memethesis\" class=\"u-url mention\">@<span>memethesis</span></a></span> :drake_dislike: Memes without emojo<br />:drake_like: :hacker_m: :hacker_e: :hacker_m: :hacker_e: :hacker_s: with such cat emojo :cate: :catto:</p>']


def uncurse(toot: str):
    # toots come in a cursed format (HTML)
    # tags like <p>, <a href=""> and <br /> may appear
    blessed = ''

    toot = sub('<\s*br\s*/?>|</p><p>', '\n', toot)
    # target: throw away anything braced with <>
    in_square_bracket = False
    for char in toot:
        if char == '<':
            in_square_bracket = True
        elif char == '>':
            in_square_bracket = False
        else:
            if not in_square_bracket:
                blessed += char
    # TODO: parse &...;
    return blessed


def memethesis(toot: str, emojis={}, instance='', saveto=''):
    blessed = uncurse(toot)
    lines = blessed.splitlines()

    """ 
    Check if is drake meme (drakeness == 2)

    Pattern:
    [arbitrary content, as caption (TODO)]
    [arbitrary content such as `@memethesis`]:drake_dislike: [arbitrary content]
    [arbitrary content, concatenated to end of dislike with a line break]
    :drake_like: [arbitrary content]
    [arbitrary content, concatenated to end of like with a line break]
    """
    # TODO: def is_drake()
    drakeness = 0
    parsed_drake = {
        'dislike': '',
        'like': '',
        'emojis': emojis,
        'instance': instance,
        'saveto': saveto if saveto else 'drake.jpg'
    }

    for line in lines:
        # if line.strip().startswith(':drake_dislike:') and drakeness == 0:
        if (not line.find(':drake_dislike:') == -1 and
            not line.strip().endswith(':drake_dislike:') and
                drakeness == 0):
            # start dislike
            drakeness += 1
            # split() string
            # '@memethesis :drake_dislike: send :drake_dislike: to people you disagree with'
            # into ['@memethesis ', ' send ', ' to people you disagree with']
            # then merge the list starting from index 1
            # with ':drake_dislike: in between each adjacent pair
            # so that it becomes ' send :drake_dislike: to people you disagree with'
            # finally strip() the leading space
            parsed_drake['dislike'] = ':drake_dislike:'.join(
                line.split(':drake_dislike:')[1:]
            ).strip()
            # TODO: limit line split to once
        elif line.strip().startswith(':drake_like:') and drakeness == 1:
            drakeness += 1
            # remove leading :drake_like:, but not the others
            parsed_drake['like'] = line.replace(':drake_like:', '', 1).strip()
        elif drakeness == 1:
            # append line to dislike
            parsed_drake['dislike'] += '\n' + line.strip()
        elif drakeness == 2:
            # append line to like
            parsed_drake['like'] += '\n' + line.strip()

    if drakeness == 2:
        # is drake meme
        make_drake(**parsed_drake)
        return 'Drake'  # return meme type

    return 'not a meme'


if __name__ == '__main__':
    # for toot in TOOTS:
        # anticipated console output:
        # not a meme
        # Drake (x4)
        # print(memethesis(toot))
    memethesis(TOOTS[-1], emojis={
        "hacker_m": "https://cdn.mastodon.technology/custom_emojis/images/000/019/658/static/8247c749af3ca0ba.png",
        "hacker_e": "https://cdn.mastodon.technology/custom_emojis/images/000/019/651/static/2fb1e9ec6c35a4e7.png",
        "hacker_s": "https://cdn.mastodon.technology/custom_emojis/images/000/019/663/static/5f3731281ddc22f9.png",
        "cate": "https://cdn.mastodon.technology/custom_emojis/images/000/074/675/static/71593e05a95bd8a7.png",
        "catto": "https://cdn.mastodon.technology/custom_emojis/images/000/082/698/static/0ed6bafb0cbb3008.png"
    }, instance='https://mastodon.technology/@fakefred/103526793891861663')
