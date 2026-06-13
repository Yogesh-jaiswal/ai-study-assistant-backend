import logging

from models.notebook import Notebook
from exceptions import DatabaseError
from app.extensions import db

# Set up logging
logger = logging.getLogger(__name__)


def notebook_owned_by_user_query(notebook_id: str, user_id: str):
    """
    Build a query that returns a notebook only if it belongs to the user.

    Used to enforce notebook ownership checks across repository methods.
    """
    return (
        db.select(Notebook)
        .where(
            Notebook.id == notebook_id,
            Notebook.user_id == user_id
        )
    )


def save_notebook(notebook: Notebook) -> None:
    """
    Persist a notebook to the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    db.session.add(notebook)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed to create notebook")
        db.session.rollback()
        raise DatabaseError("Failed to create notebook")


def get_notebook_by_notebook_id(
    notebook_id: str,
    user_id: str
) -> Notebook | None:
    """
    Retrieve a notebook by its ID and owner.

    Returns:
        The notebook if found and owned by the user, otherwise None.
    """
    notebook = db.session.scalar(
        notebook_owned_by_user_query(notebook_id, user_id)
    )

    return notebook


def get_notebook_by_user_id(user_id: str) -> list[Notebook]:
    """
    Retrieve all notebooks belonging to a user.

    Returns:
        A list of notebooks owned by the specified user.
    """
    notebooks = db.session.scalars(
        db.select(Notebook)
        .where(Notebook.user_id == user_id)
    ).all()

    return notebooks


def remove_notebook(notebook: Notebook) -> None:
    """
    Delete a notebook from the database.

    Raises:
        DatabaseError: If the delete transaction fails.
    """
    db.session.delete(notebook)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed to delete notebook")
        db.session.rollback()
        raise DatabaseError("Failed to delete notebook")


def get_notebook_with_uploads(
    notebook_id: str,
    user_id: str
) -> Notebook | None:
    """
    Retrieve a notebook with its uploads eagerly loaded.

    Returns:
        The notebook and associated uploads if found, otherwise None.
    """
    notebook = db.session.scalar(
        notebook_owned_by_user_query(notebook_id, user_id)
        .options(db.selectinload(Notebook.uploads))
    )

    return notebook


def get_notebook_with_summaries(
    notebook_id: str,
    user_id: str
) -> Notebook | None:
    """
    Retrieve a notebook with its summaries eagerly loaded.

    Returns:
        The notebook and associated summaries if found, otherwise None.
    """
    notebook = db.session.scalar(
        notebook_owned_by_user_query(notebook_id, user_id)
        .options(db.selectinload(Notebook.summaries))
    )

    return notebook