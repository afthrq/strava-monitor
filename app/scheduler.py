import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import POLL_INTERVAL_MINUTES
from app.strava.poller import run_polling_cycle

_scheduler = None

def start_scheduler():
    global _scheduler
    if _scheduler:
        return

    _scheduler = AsyncIOScheduler()

    def wrapper():
        asyncio.create_task(run_polling_cycle())

    _scheduler.add_job(wrapper, trigger="date")

    _scheduler.add_job(wrapper, "interval", minutes=POLL_INTERVAL_MINUTES)

    _scheduler.start()

    print(f"[SCHEDULER] Started — interval: {POLL_INTERVAL_MINUTES} minutes")
