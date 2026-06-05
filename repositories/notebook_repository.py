from models.notebook import Notebook
from app.extensions import db

def notebook_owned_by_user_query(notebook_id: int, user_id: int):
    """Helper function to get user notebook ownership query"""
    return (
        db.select(Notebook)
        .where(
            Notebook.id == notebook_id,
            Notebook.user_id == user_id
        )
    )