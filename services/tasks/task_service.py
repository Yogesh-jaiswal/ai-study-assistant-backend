from typing import Any

from celery.result import AsyncResult
from app.celery_app import celery_app

from services.integrations.redis_service import get_key
from exceptions import ResourceNotFoundError

def task_status(task_id: str, user_id: str) -> dict[str, Any]:
    owner = get_key(f"task:{task_id}:owner")
    task_type = get_key(f"task:{task_id}:type")
    
    if not owner or task_type or owner != user_id:
        raise ResourceNotFoundError("Unknown task id")
    
    result = AsyncResult(str(task_id), app=celery_app)

    response = {
        "task_id": task_id,
        "status": result.status,
        "type": task_type
    }

    if result.successful():
        response["result"] = result.result
    elif result.failed():
        response["error"] = str(result.result)

    return response