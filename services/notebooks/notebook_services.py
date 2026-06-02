import logging

from app.extensions import db
from models import Notebook

from exceptions import DatabaseError, ResourceNotFoundError

# Set up logging
logger = logging.getLogger(__name__)

def create_notebook(payload):
    """Creates a new notebook"""
    notebook = Notebook(title=payload.title)
    
    db.session.add(notebook)
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to create notebook: {str(e)}")
        db.session.rollback()
        raise DatabaseError(f"Failed to create notebook")
    return notebook.id

def get_notebook(notebook_id):
    """Gets a specific notebook"""
    notebook = db.session.get(Notebook, notebook_id)

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")

    return {
        "id": notebook.id,
        "title": notebook.title,
        "created_at": notebook.created_at.isoformat()
    }

def get_all_notebooks():
    """Get all notebooks"""
    notebooks = db.session.query(Notebook).all()

    return [
        {
            "id": notebook.id,
            "title": notebook.title,
            "created_at": notebook.created_at.isoformat()
        }
        for notebook in notebooks
    ]

def delete_notebook(notebook_id):
    """Deletes a specific notebook"""
    notebook = db.session.get(Notebook, notebook_id)

    if not notebook:
        raise ResourceNotFoundError(f"Notebook with id {notebook_id} not found")

    db.session.delete(notebook)
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to delete notebook: {str(e)}")
        db.session.rollback()
        raise DatabaseError(f"Failed to delete notebook")