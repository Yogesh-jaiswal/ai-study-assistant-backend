import logging

from models import Notebook, Upload
from exceptions import DatabaseError
from app.extensions import db

# # Set up logging
logger = logging.getLogger(__name__)


def save_upload(upload: Upload) -> None:
    """
    Persist an upload to the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    db.session.add(upload)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed creating upload")
        db.session.rollback()
        raise DatabaseError("Failed to create upload")


def get_upload_by_upload_id(
    notebook_id: str,
    user_id: str,
    upload_id: str
) -> Upload | None:
    """
    Retrieve an upload by ID while enforcing notebook ownership.

    Returns:
        The upload if found and owned by the user, otherwise None.
    """
    upload = db.session.scalar(
        db.select(Upload)
        .join(Notebook)
        .where(
            Upload.id == upload_id,
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )

    return upload


def remove_upload(upload: Upload) -> None:
    """
    Delete an upload from the database.

    Raises:
        DatabaseError: If the delete transaction fails.
    """
    db.session.delete(upload)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed deleting upload")
        db.session.rollback()
        raise DatabaseError("Failed to delete upload")


def get_uploads_in_group(
    upload_ids: list[str],
    notebook_id: str
) -> list[Upload]:
    """
    Retrieve a group of uploads belonging to a notebook.

    Only the upload ID and raw text fields are loaded for efficiency.
    """
    uploads = db.session.scalars(
        db.select(Upload)
        .options(db.load_only(Upload.id, Upload.raw_text))
        .where(
            Upload.notebook_id == notebook_id,
            Upload.id.in_(upload_ids)
        )
    ).all()

    return uploads