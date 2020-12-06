"""
    This module handles starting and shutting down tasks that need to be performed
    on a certain interval.
"""
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import db_utils

SCHEDULE_START_DATE = "2020-01-01 00:15:00"
SCHEDULE_TRIGGER = "interval"
SCHEDULE_INTERVAL_MINUTES = 1


def start_tasks():
    """
    Starts the scheduled tasks.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=db_utils.update_walk_ins,
        trigger=SCHEDULE_TRIGGER,
        minutes=SCHEDULE_INTERVAL_MINUTES,
        start_date=SCHEDULE_START_DATE,
    )

    scheduler.start()
    atexit.register(scheduler.shutdown)
