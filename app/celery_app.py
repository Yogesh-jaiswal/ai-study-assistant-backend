from celery import Celery

from configs import get_settings

settings = get_settings()

celery_app = Celery(
    "ai_study_assistant",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)

celery_app.conf.update(
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_TASK_EAGER_PROPAGATES,
    task_store_eager_result=True
)

print(
    f"ENV={settings.ENVIRONMENT} "
    f"ASYNC={not settings.CELERY_TASK_ALWAYS_EAGER}"
)

celery_app.conf.imports = (
    "tasks.example_tasks",
    "tasks.ai_content_task",
    "tasks.processing_task"
)