from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def get_scheduler() -> BaseScheduler:
    return AsyncIOScheduler(

    )
