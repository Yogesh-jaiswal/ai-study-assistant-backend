"""
This is a sample file to check celery and it's working.
"""

import time
from app.celery_app import celery_app as celery

@celery.task
def add_numbers(a: int, b: int) -> int:
    return a+b

@celery.task
def long_running_task() -> str:
    time.sleep(25)

    return "completed"