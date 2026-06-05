import logging
from typing import Any

from app.extensions import db
from models import Notebook

from validators.notebook_schemas import CreateNotebookRequest
from repositories.notebook_repository import notebook_owned_by_user_query

from exceptions import DatabaseError, ResourceNotFoundError

# Set up logging
logger = logging.getLogger(__name__)

def create_notebook(user_id: int, payload: CreateNotebookRequest) -> int:
    """Creates a new notebook"""
    notebook = Notebook(title=payload.title, user_id=user_id)
    
    db.session.add(notebook)
    try:
        db.session.commit()
    except Exception:
        logger.exception(f"Failed to create notebook")
        db.session.rollback()
        raise DatabaseError(f"Failed to create notebook")
    return notebook.id

def get_notebook(notebook_id: int, user_id: int) -> dict[str, Any]:
    """Gets a specific notebook"""
    notebook = db.session.scalar(notebook_owned_by_user_query(notebook_id, user_id))

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")

    return {
        "id": notebook.id,
        "title": notebook.title,
        "created_at": notebook.created_at.isoformat()
    }

def get_all_notebooks(user_id: int) -> list[dict[str, Any]]:
    """Get all notebooks"""
    notebooks = db.session.scalars(
        db.select(Notebook)
        .where(Notebook.user_id == user_id)
    ).all()

    return [
        {
            "id": notebook.id,
            "title": notebook.title,
            "created_at": notebook.created_at.isoformat()
        }
        for notebook in notebooks
    ]

def delete_notebook(notebook_id: int, user_id: int) -> None:
    """Deletes a specific notebook"""
    notebook = db.session.scalar(notebook_owned_by_user_query(notebook_id, user_id))

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")

    db.session.delete(notebook)
    try:
        db.session.commit()
    except Exception:
        logger.exception(f"Failed to delete notebook")
        db.session.rollback()
        raise DatabaseError(f"Failed to delete notebook")