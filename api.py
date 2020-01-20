import mastodon
from mastodon import Mastodon, StreamListener
from memethesis import memethesis
from os import remove
from config import *

masto = Mastodon(
    api_base_url=API_BASE_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)


def determine_visibility(vis: str) -> str:
    # only direct if incoming status is direct; else unlisted
    return 'direct' if vis == 'direct' else 'unlisted'


class Listener(StreamListener):
    def on_notification(self, ntf):
        # All your notifications are belong to us!
        if ntf['type'] == 'mention':
            # attempt to generate meme
            path = str(ntf['status']['id']) + '.jpg'
            meme_type = memethesis(
                ntf['status']['content'], saveto=path)
            if not meme_type == 'not a meme':
                # upload meme
                media_id = masto.media_post(
                    'output/' + path, mime_type='image/jpeg')['id']
                # publish toot
                masto.status_reply(
                    ntf['status'],
                    f'Here\'s your {meme_type} meme',
                    visibility=determine_visibility(
                        ntf['status']['visibility']),
                    media_ids=media_id
                )
                # log to console
                print(
                    f"Generated {meme_type} meme for status id {ntf['status']['id']}")
                # remove meme image
                remove('output/' + path)


def start_streaming():
    listener = Listener()
    masto.stream_user(listener)


if __name__ == '__main__':
    start_streaming()
