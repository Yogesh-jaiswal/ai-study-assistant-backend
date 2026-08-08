from celery import Celery

from configs import get_settings

settings = get_settings()

# Initialize Celery application with Redis as the broker and backend
celery_app = Celery(
    "ai_study_assistant",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Update Celery configuration based on settings
celery_app.conf.update(
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_TASK_EAGER_PROPAGATES,
    task_store_eager_result=True
)

# Print the current environment and whether Celery tasks are executed eagerly or asynchronously
print(
    f"ENV={settings.ENVIRONMENT} "
    f"ASYNC={not settings.CELERY_TASK_ALWAYS_EAGER}"
)

celery_app.conf.imports = (
    "tasks.example_tasks",
    "tasks.ai_content_task",
    "tasks.processing_task"
)