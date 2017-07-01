from app import models, logger
from threading import Thread, Event
import time


class Travian(Thread):
    def __init__(self, account_id):
        Thread.__init__(self)
        self.account = models.Account.query.get(account_id)
        self.shutdown = threading.Event()

    def run(self):
        logger.info('Thread #{id} <{name}> started', id=self.account.id, name=self.account.username)

        while not shutdown.is_set():
            # Thread work
            sleep(1)

        logger.info('Thread #{id} <{name}> stopped', id=self.account.id, name=self.account.username)


travian_threads = [Travian(account.id) for account in models.Account.query.all()]


def stop_jobs():
    for thr in travian_threads:
        thr.shutdown.set()

    for thr in travian_threads:
        thr.join()


for thread in travian_threads:
    thread.start()
