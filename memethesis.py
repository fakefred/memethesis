from re import sub
from drake import make_drake

# TOOT = '<p>drake + <br />:drake_dislike: dislike<br />:drake_like: desliek<br /><a href="https://mastodon.technology/tags/tag" class="mention hashtag" rel="tag">#<span>tag</span></a></p>'
# TOOT = ':drake_dislike: Cable News Network <br /> :drake_like: Convolutionary Neural Network'
TOOT = '<p><span class="h-card"><a href="https://botsin.space/@memethesis" class="u-url mention" rel="nofollow noopener" target="_blank">@<span>memethesis</span></a></span>:drake_dislike: Run bot on proper server<br>:drake_like: Run bot on VS Code</p>'


def uncurse(toot: str):
    # toots come in a cursed format (HTML)
    # tags like <p>, <a href=""> and <br /> may appear
    blessed = ''

    toot = sub('<\s*br\s*/?>', '\n', toot)
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


def memethesis(toot: str, saveto=''):
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

    drakeness = 0
    parsed_drake = {
        'dislike': '',
        'like': '',
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
        elif line.strip().startswith(':drake_like:') and drakeness == 1:
            drakeness += 1
            parsed_drake['like'] = line.replace(':drake_like:', '').strip()
        elif drakeness == 1:
            # in dislike
            parsed_drake['dislike'] += '\n' + line.strip()
        elif drakeness == 2:
            # in like
            parsed_drake['like'] += '\n' + line.strip()

    if drakeness == 2:
        # is drake meme
        make_drake(**parsed_drake)
        return 'Drake'  # return meme type


if __name__ == '__main__':
    memethesis(TOOT)
