from mastodon import Mastodon
from memethesis import memethesis
from datetime import datetime, timedelta, timezone
from os import remove
from config import *

masto = Mastodon(
    api_base_url=API_BASE_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)


def is_recent(time: datetime) -> bool:
    if timedelta() < datetime.now(timezone.utc) - time <= timedelta(minutes=RECENT_THRESHOLD):
        return True
    return False


def poll():
    notifs = masto.notifications()
    id_file = open('./logs/responded.log', 'r')
    id_list = id_file.readlines()
    id_list = [int(line.strip()) for line in id_list]
    id_file.close()

    id_file = open('./logs/responded.log', 'a')
    for ntf in notifs:
        if ntf['type'] == 'mention':
            # the notif is recent and unread by drakebot
            if is_recent(ntf['status']['created_at']) and ntf['status']['id'] not in id_list:
                path = str(ntf['status']['id']) + '.jpg'
                # generate meme
                meme_type = memethesis(ntf['status']['content'], saveto=path)
                # upload meme
                media_id = masto.media_post(
                    'output/' + path, mime_type='image/jpeg')['id']
                # publish toot
                masto.status_reply(
                    ntf['status'],
                    f'Here\'s your {meme_type} meme',
                    visibility='unlisted',
                    # visibility='direct',
                    media_ids=media_id
                )
                # log to console
                print(f"Generated {meme_type} meme for status id {ntf['status']['id']}")
                # set read
                id_file.writelines(str(ntf['status']['id']) + '\n')
                # remove meme image
                remove('output/' + path)

    id_file.close()


if __name__ == '__main__':
    poll()
