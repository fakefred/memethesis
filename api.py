from mastodon import Mastodon, StreamListener
from memethesis import prepare, memethesis
from emojiops import construct_emoji_dict
from config import *
from fontconfig import LANGS, FONTS
from os import remove
from datetime import datetime, timezone
from threading import Timer


masto = Mastodon(
    api_base_url=API_BASE_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)

# record for rate limit
record = {}


def time_string() -> str:
    # 2020-01-29 12:30:34|.957996+00:00
    # <--   splice    -->| HACK
    return str(datetime.now(timezone.utc))[:19]


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


def handle_toot(status, trace=False, visibility='', reply_to=None) -> bool:
    '''
    trace: denotes whether the memethesis was requested by the original
    poster of the text format meme, or a third account. In the latter case,
    the rate limit record is raised for the third account, not the OP.
    Of course, the OP themselves could request a memethesis, but we assume
    it is a third account just to be unambigious.

    visibility: that of the status to send

    reply_to: status to reply to

    returns bool: True if `status` is a meme.
    '''
    # reject if account is of a bot, unless this is a traced handle request
    if status['account']['bot'] and not trace:
        return  # UNTESTED

    sid = status['id']
    path = str(sid) + '.jpg'
    # @handle[@domain]; uniqueness guaranteed
    acct = status['account']['acct']

    meme_type, info = prepare(
        status['content'],
        emojis=construct_emoji_dict(status['emojis']),
        instance=status['url'],  # emojiops.py will handle this
        saveto=path
    )

    if meme_type == 'not a meme':
        return False

    elif meme_type == 'language not supported':
        supported_languages = ', '.join(LANGS.keys())
        masto.status_reply(
            status,
            f'Sorry, the language you specified is not yet supported. \
You can Delete and Redraft the post changing your language to one of these: \
{supported_languages}.',
            visibility=determine_visibility(
                status['visibility']) if not visibility else visibility
        )
        print(f'{time_string()}: Language not supported, status id {sid} by {acct}')
        return False

    elif meme_type == 'font not supported':
        supported_fonts = ', '.join(FONTS.keys())
        masto.status_reply(
            status,
            f'Sorry, the language you specified is not yet supported. \
You can Delete and Redraft the post changing your font to one of these: \
{supported_fonts}.'
        )
        print(f'{time_string()}: Font not supported, status id {sid} by {acct}')
        return False

    elif not meme_type == 'empty':
        if not within_limit(acct):
            # hit rate limit
            masto.status_reply(
                status if reply_to is None else reply_to,
                f'Sorry, you have triggered my rate limiting mechanism. \
This is not serious (at all). Please try again in at most {RATELIMIT_TIME} minutes.',
                visibility=(determine_visibility(status['visibility'])
                            if not visibility else visibility)
            )
            print(f'{time_string()}: Account {acct} hit their limit, status id {sid}')
            return False  # exit method, refuse to generate meme
        # generate meme
        memethesis(meme_type, info)
        # upload meme
        media_id = masto.media_post(
            'output/' + path, mime_type='image/jpeg')['id']
        # publish toot
        masto.status_reply(
            status if reply_to is None else reply_to,
            f'Here\'s your {meme_type} meme',
            visibility=determine_visibility(
                status['visibility']) if not visibility else visibility,
            media_ids=media_id
        )
        # log to console
        print(
            f'{time_string()}: Generated {meme_type} meme for status id {sid} by {acct}')

        if not trace:
            # log this memethesis into volatile memory for rate limiting
            if acct in record:
                record[acct] += 1
            else:
                record[acct] = 1
            # trigger erase_one_from_record(acct) in several minutes
            Timer(RATELIMIT_TIME * 60.0,
                  erase_one_from_record, [acct]).start()

        # remove meme image
        try:
            remove('output/' + path)
        except FileNotFoundError:
            pass  # better than crashing completely
        return True

    elif meme_type == 'empty':
        # attempt memethesis for parent post
        # fear not, is not de facto recursion
        parent_id = status['in_reply_to_id']  # None if status is top-level
        if parent_id is not None:
            is_meme = handle_toot(
                masto.status(parent_id),
                visibility=status['visibility'],
                reply_to=status  # *this* status by third account, not parent
            )
            if is_meme:
                # this part is essentially the same as above
                # except this time acct is the account who requested the memethesis
                # i.e. the one who sent the bot an empty status
                if acct in record:
                    record[acct] += 1
                else:
                    record[acct] = 1
                Timer(RATELIMIT_TIME * 60.0,
                      erase_one_from_record, [acct]).start()

        else:
            return False


class Listener(StreamListener):
    def on_notification(self, ntf):
        # All your notifications are belong to us!
        if ntf['type'] == 'mention':
            handle_toot(ntf['status'])


def start_streaming():
    listener = Listener()
    masto.stream_user(listener)


if __name__ == '__main__':
    start_streaming()
