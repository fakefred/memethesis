# This script serves as a debugging alternative to api.py.
# This script doesn't listen to the notification stream.
# Instead, it gets a status and runs memethesis with it
# without replying or removing the generated image
# for prolonged and iterative testing, with no risk of
# challenging the antispam mechanism, or interrupting the
# deployed memethesis instance.
from mastodon import Mastodon
from memethesis import prepare, memethesis
from emojiops import construct_emoji_dict
from config import *
from sys import argv

masto = Mastodon(
    api_base_url=API_BASE_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)


def pseudo_memethesis(id: int):
    status = masto.status(id)
    sid = status['id']
    acct = status['account']['acct']
    path = str(sid) + '.jpg'
    meme_type, info = prepare(
        status['content'],
        emojis=construct_emoji_dict(status['emojis']),
        instance=status['url'],  # emojiops.py will handle this
        saveto=path
    )
    if meme_type == 'not a meme':
        return
    elif meme_type == 'language not supported':
        supported_languages = ', '.join(LANGS.keys())
        print(f'Language not supported, status id {sid} by {acct}')
        return
    else:
        # generate meme
        memethesis(meme_type, info).show()
        # log to console
        print(
            f"Generated {meme_type} meme for status id {sid} by {acct}")


if __name__ == '__main__':
    pseudo_memethesis(int(argv[1]))
