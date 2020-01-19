from api import poll
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':
    # create interval scheduler for mastodon
    sch = BackgroundScheduler()
    sch.add_job(poll, 'interval', seconds=30)
    sch.start()
    try:
        while True:
            sleep(2)
    except (KeyboardInterrupt, SystemExit):
        sch.shutdown()
