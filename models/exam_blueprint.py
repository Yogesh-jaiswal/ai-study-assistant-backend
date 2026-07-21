import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class ExamBlueprint(db.Model):
    __tablename__ = "exam_blueprints"

    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    slug: Mapped[str] = mapped_column(
        db.String,
        unique=True,
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        db.String(200), 
        nullable=False
    )
    
    description: Mapped[str] = mapped_column(
        db.String,
        nullable=True
    )

    created_by: Mapped[str] = mapped_column(
        db.ForeignKey("users.id"),
        nullable=True
    )

    is_public: Mapped[bool] = mapped_column(
        db.Boolean,
        default=lambda: False,
        nullable=False
    )

    is_system: Mapped[bool] = mapped_column(
        db.Boolean,
        default=lambda: False,
        nullable=False
    )

    structure: Mapped[dict] = mapped_column(
        db.JSON,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user: Mapped["User"] = db.relationship("User", back_populates="blueprints", lazy="raise_on_sql")