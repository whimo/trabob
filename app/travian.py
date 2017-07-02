from app import models
from threading import Thread, Event
import time


class Travian(Thread):
    def __init__(self, account_id):
        Thread.__init__(self)
        self.account = models.Account.query.get(account_id)
        self.shutdown = Event()

    def run(self):
        print('[INFO] Thread #{} <{}> started'.format(self.account.id, self.account.username))

        while not self.shutdown.is_set():
            # Thread work
            time.sleep(4)

        print('[INFO] Thread #{id} <{name}> stopped'.format(self.account.id, self.account.username))


travian_threads = [Travian(account.id) for account in models.Account.query.all()]


def stop_jobs():
    for thr in travian_threads:
        thr.shutdown.set()

    for thr in travian_threads:
        thr.join()


for thread in travian_threads:
    thread.start()
