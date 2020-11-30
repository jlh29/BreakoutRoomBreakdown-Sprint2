"""
    This module handles starting and shutting down tasks that need to be performed
    on a certain interval.
"""
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import db_utils


def start_tasks():
    """
    Starts the scheduled tasks.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=db_utils.update_walk_ins,
        trigger="interval",
        minutes=1,
        start_date="2020-01-01 00:15:00",
    )

    scheduler.start()
    atexit.register(scheduler.shutdown)
