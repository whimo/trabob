from app import models, logger
from threading import Thread, Event
import time
import datetime
import random


class Travian(Thread):
    def __init__(self, account_id):
        Thread.__init__(self)
        self.account = models.Account.query.get(account_id)
        self.shutdown = Event()

    def run(self):
        logger.info('Thread #{} <{}> started'.format(self.account.id, self.account.username))

        while not self.shutdown.is_set():
            if self.account.busy_until is None:
                self.account.get_busy_until()

            if datetime.datetime.utcnow() > self.account.busy_until:
                time.sleep(random.randint(10, 60))  # Sleep a bit to avoid being caught on automated requests
                try:
                    self.account.build(self.account.build_queue.pop())
                except IndexError:
                    logger.info('Empty build queue for {}.'.format(self.account.username))

        logger.info('Thread #{id} <{name}> stopped'.format(self.account.id, self.account.username))


travian_threads = [Travian(account.id) for account in models.Account.query.all()]


def stop_jobs():
    for thr in travian_threads:
        thr.shutdown.set()

    for thr in travian_threads:
        thr.join()


for thread in travian_threads:
    thread.start()
