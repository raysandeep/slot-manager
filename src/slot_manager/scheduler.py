from apscheduler.schedulers.background import BackgroundScheduler
from .load_manager import LoadManager
from .constants import CRON_INTERVAL_MINUTES


class Scheduler:
    def __init__(self, manager: LoadManager):
        self.manager = manager
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.add_job(self.manager.reconcile, 'interval', minutes=CRON_INTERVAL_MINUTES)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()
