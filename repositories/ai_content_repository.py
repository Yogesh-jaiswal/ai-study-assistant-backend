import logging

from app.extensions import db
from models import (
    Notebook,
    AIContent,
    UploadAIContentRelationship
)
from exceptions import DatabaseError

# Set up logging
logger = logging.getLogger(__name__)


def save_ai_content(ai_content: AIContent, uploads_ids: list[str]) -> None:
    """
    Persist an ai content and its upload relationships in a single transaction.

    Raises:
        DatabaseError: If creating the ai content or relationships fails.
    """
    try:
        db.session.add(ai_content)
        db.session.flush()

        relationships = [
            UploadAIContentRelationship(
                upload_id=upload_id,
                ai_content_id=ai_content.id
            )
            for upload_id in uploads_ids
        ]

        db.session.add_all(relationships)
        db.session.commit()

    except Exception:
        logger.exception(
            "Failed creating ai content or relationships"
        )
        db.session.rollback()
        raise DatabaseError(
            "Failed to create ai content or relationships"
        )


def get_all_ai_contents_by_notebook_id(
        notebook_id: str,
        user_id: str,
        limit: int,
        offset: int
) -> list[AIContent]:
    """
    Retrieve all ai content under a notebook.

    Returns:
        List of ai contents if notebook found otherwise empty list.
    """

    return db.session.scalars(
        db.select(AIContent)
        .join(Notebook)
        .where(
            Notebook.id == notebook_id,
            Notebook.user_id == user_id
        )
        .order_by(
            AIContent.generated_at.desc()
        )
        .limit(limit)
        .offset(offset)
    ).all()


def get_ai_content_by_content_id(
    notebook_id: str,
    user_id: str,
    ai_content_id: str
) -> AIContent | None:
    """
    Retrieve an ai content by ID while enforcing notebook ownership.

    Returns:
        The ai content if found and owned by the user, otherwise None.
    """
    ai_content = db.session.scalar(
        db.select(AIContent)
        .join(Notebook)
        .where(
            AIContent.id == ai_content_id,
            AIContent.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )

    return ai_content


def remove_ai_content(ai_content: AIContent) -> None:
    """
    Delete an ai content from the database.

    Raises:
        DatabaseError: If the delete transaction fails.
    """
    db.session.delete(ai_content)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed deleting ai content")
        db.session.rollback()
        raise DatabaseError("Failed to delete ai content")