import logging
from shutil import rmtree
from pathlib import Path
from typing import Any

from models import Notebook

from validators.notebook_schemas import CreateNotebookRequest
from repositories.notebook_repository import (
    save_notebook,
    get_notebook_by_notebook_id,
    get_notebook_by_user_id,
    remove_notebook,
    update_notebook
)
from configs import get_settings

from exceptions import ResourceNotFoundError

def create_notebook(user_id: str, payload: CreateNotebookRequest) -> str:
    """Creates a new notebook"""
    notebook = Notebook(title=payload.title, user_id=user_id)
    
    save_notebook(notebook)

    return notebook.id

def get_notebook(notebook_id: str, user_id: str) -> dict[str, Any]:
    """Gets a specific notebook"""
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")

    return {
        "id": notebook.id,
        "title": notebook.title,
        "created_at": notebook.created_at.isoformat()
    }

def get_all_notebooks(user_id: str, limit: int = 20 , offset: int = 0) -> list[dict[str, Any]]:
    """Get all notebooks"""
    notebooks = get_notebook_by_user_id(user_id, limit, offset)

    return [
        {
            "id": notebook.id,
            "title": notebook.title,
            "created_at": notebook.created_at.isoformat()
        }
        for notebook in notebooks
    ]

def edit_notebook(notebook_id: str, user_id: str, payload: CreateNotebookRequest) -> None:
    """Edit a specific notebook"""
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")
    
    notebook.title = payload.title

    update_notebook(notebook)

    return notebook.id


def delete_notebook(notebook_id: str, user_id: str) -> None:
    """Deletes a specific notebook"""
    notebook = get_notebook_by_notebook_id(notebook_id, user_id)

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")
    
    upload_dir = Path(get_settings().UPLOAD_FOLDER) / str(notebook.id)

    if upload_dir.exists():
        rmtree(upload_dir)

    remove_notebook(notebook)