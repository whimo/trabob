from app import models
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
        print('[INFO] Thread #{} <{}> started'.format(self.account.id, self.account.username))

        while not self.shutdown.is_set():
            if self.account.busy_until is None:
                self.account.get_busy_until()

            if datetime.datetime.utcnow() > self.account.busy_until:
                time.sleep(random.randint(10, 60))  # Sleep a bit to avoid being caught on automated requests
                try:
                    for item in self.account.build_queue:
                        if self.account.build(item):
                            account.build_queue.remove(item)
                            break

                    if self.account.is_roman:
                        for item in self.account.resources_build_queue:
                            if self.account.build(item):
                                account.resources_build_queue.remove(item)
                                break

                except IndexError:
                    print('[INFO] Empty build queue for {}.'.format(self.account.username))

        print('[INFO] Thread #{id} <{name}> stopped'.format(self.account.id, self.account.username))


travian_threads = [Travian(account.id) for account in models.Account.query.all()]


def stop_jobs():
    for thr in travian_threads:
        thr.shutdown.set()

    for thr in travian_threads:
        thr.join()


for thread in travian_threads:
    thread.start()
