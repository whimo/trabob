from app import models
from threading import Thread
import time


class Travian(Thread):
    def __init__(self, account_id):
        Thread.__init__(self)
        self.account = models.Account.query.get(account_id)

    def run(self):
        while True:
            # Mainloop will be here
            time.sleep(4)


travian_threads = [Travian(account.id) for account in models.Account.query.all()]

for thread in travian_threads:
    thread.start()
