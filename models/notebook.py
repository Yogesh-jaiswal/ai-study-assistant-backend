from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .summary import Summary
    from .uploads import Upload

class Notebook(db.Model):
    __tablename__ = "notebooks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        db.String(200),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    upload: Mapped[list["Upload"]] = db.relationship("Upload", back_populates="notebook", cascade="all, delete-orphan", lazy="raise_on_sql")
    summary: Mapped[list["Summary"]] = db.relationship("Summary", back_populates="notebook", cascade="all, delete-orphan", lazy="raise_on_sql")