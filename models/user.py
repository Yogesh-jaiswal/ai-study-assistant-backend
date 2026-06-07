from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .notebook import Notebook
    from .refresh_token import RefreshToken

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        db.String(50), 
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        db.String(100),
        unique=True, 
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = db.relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan", lazy="raise_on_sql")
    notebooks: Mapped[list["Notebook"]] = db.relationship("Notebook", back_populates="user", cascade="all, delete-orphan", lazy="raise_on_sql")