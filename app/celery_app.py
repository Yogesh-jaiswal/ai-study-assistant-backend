from celery import Celery

from app import create_app
from configs import get_settings

settings = get_settings()

flask_app = create_app()

celery_app = Celery(
    "ai_study_assistant",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)

celery_app.conf.imports = (
    "tasks.example_task",
    "tasks.summary_task"
)