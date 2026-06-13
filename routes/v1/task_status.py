from uuid import UUID

from flask import jsonify, g
from pydantic import BaseModel
from services.tasks.task_service import task_status

from . import v1_bp
from decorators import login_required

# Task path parameters model
class TaskPath(BaseModel):
    task_id: UUID

# Returns a task status
@v1_bp.get(
    "/tasks/<string:task_id>",
)
@login_required
def get_tasks_status(path: TaskPath):
    """Endpoint to get the task status"""
    response = task_status(str(path.task_id), g.user_id)

    return jsonify(response)