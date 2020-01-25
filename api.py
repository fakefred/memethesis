from mastodon import Mastodon, StreamListener
from memethesis import prepare, memethesis
from emojiops import construct_emoji_dict
from os import remove
from threading import Timer
from config import *


masto = Mastodon(
    api_base_url=API_BASE_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)

# record for rate limit
record = {}


def erase_one_from_record(account: str):
    # erase one record off an account
    if account in record:
        record[account] -= 1


def within_limit(account: str) -> bool:
    if account in record:
        if record[account] <= RATELIMIT_NUM:
            return True  # has record, within
        return False  # has record, exceeded
    return True  # no record


def determine_visibility(vis: str) -> str:
    # only direct if incoming status is direct; else unlisted
    return 'direct' if vis == 'direct' else 'unlisted'


class Listener(StreamListener):
    def on_notification(self, ntf):
        # All your notifications are belong to us!
        if ntf['type'] == 'mention':
            status = ntf['status']
            path = str(status['id']) + '.jpg'
            # @handle[@domain]; uniqueness guaranteed
            acct = status['account']['acct']

            meme_type, info = prepare(
                status['content'],
                emojis=construct_emoji_dict(status['emojis']),
                instance=status['url'],  # emojiops.py will handle this
                saveto=path
            )

            if not meme_type == 'not a meme':
                if not within_limit(acct):
                    # hit rate limit
                    masto.status_reply(
                        status,
                        f'Sorry, you have triggered my rate limiting mechanism. This is not serious (at all). Please try again in at most {RATELIMIT_TIME} minutes.',
                        visibility=determine_visibility(status['visibility'])
                    )
                    print(f'Account {acct} hit their limit')
                    return  # exit method, refuse to generate meme

                # generate meme
                memethesis(meme_type, info)

                # upload meme
                media_id = masto.media_post(
                    'output/' + path, mime_type='image/jpeg')['id']

                # publish toot
                masto.status_reply(
                    status,
                    f'Here\'s your {meme_type} meme',
                    visibility=determine_visibility(status['visibility']),
                    media_ids=media_id
                )

                # log to console
                print(
                    f"Generated {meme_type} meme for status id {status['id']} by {acct}")

                # log this memethesis into volatile memory for rate limiting
                if acct in record:
                    record[acct] += 1
                else:
                    record[acct] = 1
                # trigger erase_one_from_record(acct) in several minutes
                Timer(RATELIMIT_TIME * 60.0, erase_one_from_record, [acct]).start()

                # remove meme image
                remove('output/' + path)


def start_streaming():
    listener = Listener()
    masto.stream_user(listener)


if __name__ == '__main__':
    start_streaming()
