import logging

from models import ExamBlueprint
from exceptions import DatabaseError
from app.extensions import db

# # Set up logging
logger = logging.getLogger(__name__)


def save_blueprint(blueprint: ExamBlueprint) -> None:
    """
    Persist a blueprint to the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    db.session.add(blueprint)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed creating blueprint")
        db.session.rollback()
        raise DatabaseError("Failed to create blueprint")


def get_blueprint_by_blueprint_slug(
    slug: str,
    owner_id: str
) -> ExamBlueprint | None:
    """
    Retrieve a blueprint by slug while enforcing ownership or public availability.

    Returns:
        The blueprint if found and owned by the user or publicly available, otherwise None.
    """
    blueprint = db.session.scalar(
        db.select(ExamBlueprint)
        .where(
            ExamBlueprint.slug == slug,
            db.or_(
                ExamBlueprint.is_system == True,
                ExamBlueprint.is_public == True,
                ExamBlueprint.created_by == owner_id
            )
        )
    )

    return blueprint

def list_blueprints(
    *,
    owner_id: str | None = None,
    public_only: bool = False,
    keyword: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[ExamBlueprint]:
    """
    Retrieve a blueprint by ID while enforcing multiple provided filters.

    Returns:
        The list of blueprints which satisfies the filters, otherwise empty list.
    """

    query = db.select(ExamBlueprint)

    query = query.where(
        ExamBlueprint.is_system.is_(False)
    )

    if owner_id is not None:
        query = query.where(
            ExamBlueprint.created_by == owner_id
        )

    if public_only:
        query = query.where(
            ExamBlueprint.is_public.is_(True)
        )

    if keyword:
        pattern = f"%{keyword}%"

        query = query.where(
            db.or_(
                ExamBlueprint.name.ilike(pattern),
                ExamBlueprint.description.ilike(pattern),
            )
        )

    query = query.order_by(
        ExamBlueprint.name,
        ExamBlueprint.created_at.desc()
    )

    if offset:
        query.offset(offset)

    if limit:
        query.limit(limit)

    return db.session.scalars(query).all()

def remove_blueprint(blueprint: ExamBlueprint) -> None:
    """
    Delete a blueprint from the database.

    Raises:
        DatabaseError: If the delete transaction fails.
    """
    db.session.delete(blueprint)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed deleting blueprint")
        db.session.rollback()
        raise DatabaseError("Failed to delete blueprint")

def update_blueprint(blueprint: ExamBlueprint) -> None:
    """
    Update a blueprint from the database.

    Raises:
        DatabaseError: If the blueprint transaction fails.
    """
    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed to update blueprint")
        db.session.rollback()
        raise DatabaseError("Failed to update blueprint")

def list_matching_slugs(base_slug: str) -> list[str]:
    """Returns all the matching slugs"""
    return list(
        db.session.scalars(
            db.select(ExamBlueprint.slug)
            .where(
                ExamBlueprint.slug.like(f"{base_slug}%")
            )
        )
    )