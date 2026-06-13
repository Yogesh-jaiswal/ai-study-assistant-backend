import logging

from app.extensions import db
from models import (
    Notebook,
    Upload,
    Summary,
    UploadSummaryRelationship
)
from exceptions import DatabaseError

# Set up logging
logger = logging.getLogger(__name__)


def save_summary(summary: Summary, uploads: list[Upload]) -> None:
    """
    Persist a summary and its upload relationships in a single transaction.

    Raises:
        DatabaseError: If creating the summary or relationships fails.
    """
    try:
        db.session.add(summary)
        db.session.flush()

        relationships = [
            UploadSummaryRelationship(
                upload_id=upload.id,
                summary_id=summary.id
            )
            for upload in uploads
        ]

        db.session.add_all(relationships)
        db.session.commit()

    except Exception:
        logger.exception(
            "Failed creating summary"
        )
        db.session.rollback()
        raise DatabaseError(
            "Failed to create summary and relationships"
        )


def get_summary_by_summary_id(
    notebook_id: str,
    user_id: str,
    summary_id: str
) -> Summary | None:
    """
    Retrieve a summary by ID while enforcing notebook ownership.

    Returns:
        The summary if found and owned by the user, otherwise None.
    """
    summary = db.session.scalar(
        db.select(Summary)
        .join(Notebook)
        .where(
            Summary.id == summary_id,
            Summary.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )

    return summary


def remove_summary(summary: Summary) -> None:
    """
    Delete a summary from the database.

    Raises:
        DatabaseError: If the delete transaction fails.
    """
    db.session.delete(summary)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed deleting summary")
        db.session.rollback()
        raise DatabaseError("Failed to delete summary")