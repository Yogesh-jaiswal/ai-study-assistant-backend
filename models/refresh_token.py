import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        db.String,
        db.ForeignKey("users.id"),
        nullable=False
    )

    token_hash: Mapped[str] = mapped_column(
        db.String(64),
        nullable=False,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        nullable=False
    )

    user: Mapped["User"] = db.relationship("User", back_populates="refresh_tokens", lazy="raise_on_sql")