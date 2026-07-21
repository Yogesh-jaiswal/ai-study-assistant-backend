import uuid
from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

from .enums import AIContentTypes

if TYPE_CHECKING:
    from .upload_ai_content_relationship import UploadAIContentRelationship
    from .notebook import Notebook
    from .user_attempt import UserAttempt

class AIContent(db.Model):
    __tablename__ = "ai_contents"

    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    notebook_id: Mapped[str] = mapped_column(
        db.ForeignKey("notebooks.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        db.String(200),
        nullable=False
    )

    content_type: Mapped[AIContentTypes] = mapped_column(
        db.Enum(AIContentTypes),
        nullable=False
    )

    upload_count: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False
    )

    content: Mapped[dict] = mapped_column(
        db.JSON,
        nullable=False
    )

    generated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    notebook: Mapped["Notebook"] = db.relationship("Notebook", back_populates="ai_contents", lazy="raise_on_sql")
    upload_ai_content_relationships: Mapped[List["UploadAIContentRelationship"]] = db.relationship(
        back_populates="ai_content",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )
    attempts: Mapped[List["UserAttempt"]] = db.relationship(
        back_populates="ai_content",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )