import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

from .enums import ProcessingStatus, EvaluationTypes

if TYPE_CHECKING:
    from .ai_content import AIContent

class UserAttempt(db.Model):
    __tablename__ = "user_attempts"

    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    content_id: Mapped[str] = mapped_column(
        db.ForeignKey("ai_contents.id"),
        nullable=False,
        index=True
    )

    status: Mapped[ProcessingStatus] = mapped_column(
        db.Enum(ProcessingStatus),
        nullable=False,
        index=True
    )

    total_marks: Mapped[int] = mapped_column(
        db.Integer,
        nullable=True
    )

    obtained_marks: Mapped[int] = mapped_column(
        db.Integer,
        nullable=True
    )

    percentage: Mapped[float] = mapped_column(
        db.Double,
        nullable=True
    )

    evaluation_type: Mapped[EvaluationTypes] = mapped_column(
        db.Enum(EvaluationTypes),
        nullable=False,
        index=True
    )

    evaluation: Mapped[dict] = mapped_column(
        db.JSON,
        nullable=False
    )

    evaluated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    ai_content: Mapped["AIContent"] = db.relationship("AIContent", back_populates="attempts", lazy="raise_on_sql")