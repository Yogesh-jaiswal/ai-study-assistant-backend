from uuid import UUID

from flask import jsonify, g
from services.task_status.task_service import task_status
from utils.response_envelopes import create_success_response

from . import v1_bp
from decorators.login_required import login_required

# Returns a task status
@v1_bp.get("/tasks/<uuid:task_id>")
@login_required
def get_tasks_status(task_id: UUID):
    """Endpoint to get the task status"""
    response = task_status(str(task_id), g.user_id)

    return jsonify(create_success_response(response))