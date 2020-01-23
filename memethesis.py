from re import sub
from drake import make_drake
from emojiops import construct_emoji_dict



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
    
    # parse HTML encoding
    blessed = blessed.replace(
        '&amp;', '&'
    ).replace(
        '&lt;', '<'
    ).replace(
        '&gt;', '>'
    )
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
        print('Generating Drake meme')
        make_drake(**parsed_drake)
        return 'Drake'  # return meme type

    return 'not a meme'


if __name__ == '__main__':
    # Test toots
    TOOTS = ['<p>stole some emotes from .social while they werent lookin</p><p>:birdsite: :angery: :breathe: :gnomed: :dab: :thaenkin: :thinkhappy: :tinking:</p>',
         '<p>drake + <br />:drake_dislike: dislike<br />:drake_like: desliek<br /><a href="https://mastodon.technology/tags/tag" class="mention hashtag" rel="tag">#<span>tag</span></a></p>',
         ':drake_dislike: Cable News Network <br /> :drake_like: Convolutionary Neural Network',
         '<p><span class="h-card"><a href="https://botsin.space/@memethesis" class="u-url mention" rel="nofollow noopener" target="_blank">@<span>memethesis</span></a></span>:drake_dislike: Run bot on proper server<br>:drake_like: Run bot on VS Code</p>',
         '<p><span class="h-card"><a href="https://botsin.space/@memethesis" class="u-url mention">@<span>memethesis</span></a></span> :drake_dislike: Having enough prudence not to have the bot run unattended in its alpha phase</p><p>:drake_like: Running the bot overnight in gnu screen while I go to sleep</p>',
         '<p><span class=\"h-card\"><a href=\"https://botsin.space/@memethesis\" class=\"u-url mention\">@<span>memethesis</span></a></span> :drake_dislike: Memes without emojo<br />:drake_like: :hacker_m: :hacker_e: :hacker_m: :hacker_e: :hacker_s: with such cat emojo :cate: :catto:</p>',
         '<p><span class=\"h-card\"><a href=\"https://botsin.space/@memethesis\" class=\"u-url mention\">@<span>memethesis</span></a></span> :drake_dislike: :hacker_w:​:hacker_i:​:hacker_l:​:hacker_l:​ :hacker_m:​:hacker_e:​:hacker_m:​:hacker_e:​:hacker_t:​:hacker_h:​:hacker_e:​:hacker_s:​:hacker_i:​:hacker_s:​ :hacker_e:​:hacker_x:​:hacker_p:​:hacker_l:​:hacker_o:​:hacker_d:​:hacker_e:​ :hacker_w:​:hacker_h:​:hacker_e:​:hacker_n:​ :hacker_f:​:hacker_e:​:hacker_d:​ :hacker_a:​ :hacker_l:​:hacker_o:​:hacker_t:​ :hacker_o:​:hacker_f:​ :hacker_e:​:hacker_m:​:hacker_o:​:hacker_j:​:hacker_o:​?<br />:drake_like: I sure hope not!</p>']

    # for toot in TOOTS:
        # anticipated console output:
        # not a meme
        # Drake (x4)
        # print(memethesis(toot))
    memethesis(TOOTS[-1], emojis=construct_emoji_dict([{"shortcode":"drake_dislike","url":"https://cdn.mastodon.technology/custom_emojis/images/000/036/147/original/481369056bfbd567.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/036/147/static/481369056bfbd567.png","visible_in_picker":True},{"shortcode":"hacker_w","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/669/original/6821f301c0555799.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/669/static/6821f301c0555799.png","visible_in_picker":True},{"shortcode":"hacker_i","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/667/original/55f04f11c460efac.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/667/static/55f04f11c460efac.png","visible_in_picker":True},{"shortcode":"hacker_l","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/657/original/676f1ddc56513f83.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/657/static/676f1ddc56513f83.png","visible_in_picker":True},{"shortcode":"hacker_m","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/658/original/8247c749af3ca0ba.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/658/static/8247c749af3ca0ba.png","visible_in_picker":True},{"shortcode":"hacker_e","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/651/original/2fb1e9ec6c35a4e7.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/651/static/2fb1e9ec6c35a4e7.png","visible_in_picker":True},{"shortcode":"hacker_t","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/664/original/3ac6de10555a723b.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/664/static/3ac6de10555a723b.png","visible_in_picker":True},{"shortcode":"hacker_h","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/654/original/c6da1654a240fee6.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/654/static/c6da1654a240fee6.png","visible_in_picker":True},{"shortcode":"hacker_s","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/663/original/5f3731281ddc22f9.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/663/static/5f3731281ddc22f9.png","visible_in_picker":True},{"shortcode":"hacker_x","url":"https://cdn.mastodon.technology/custom_emojis/images/000/070/251/original/eaa218fb5eb87c12.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/070/251/static/eaa218fb5eb87c12.png","visible_in_picker":True},{"shortcode":"hacker_p","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/661/original/c2ba7419d669762e.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/661/static/c2ba7419d669762e.png","visible_in_picker":True},{"shortcode":"hacker_o","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/660/original/76b0925ff7d431b9.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/660/static/76b0925ff7d431b9.png","visible_in_picker":True},{"shortcode":"hacker_d","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/650/original/58505ae355bff82b.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/650/static/58505ae355bff82b.png","visible_in_picker":True},{"shortcode":"hacker_n","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/659/original/0887c9cc7bfe3b13.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/659/static/0887c9cc7bfe3b13.png","visible_in_picker":True},{"shortcode":"hacker_f","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/652/original/7627d2cda1a6f90f.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/652/static/7627d2cda1a6f90f.png","visible_in_picker":True},{"shortcode":"hacker_a","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/647/original/118ad11fae7e3477.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/647/static/118ad11fae7e3477.png","visible_in_picker":True},{"shortcode":"hacker_j","url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/655/original/6b9e292d3a603f2b.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/019/655/static/6b9e292d3a603f2b.png","visible_in_picker":True},{"shortcode":"drake_like","url":"https://cdn.mastodon.technology/custom_emojis/images/000/036/148/original/1c1a5daf467392a0.png","static_url":"https://cdn.mastodon.technology/custom_emojis/images/000/036/148/static/1c1a5daf467392a0.png","visible_in_picker":True}]), instance='https://mastodon.technology/@fakefred/103526793891861663')
