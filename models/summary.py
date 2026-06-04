from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .upload_summary_relationship import UploadSummaryRelationship
    from .notebook import Notebook

class Summary(db.Model):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    notebook_id: Mapped[int] = mapped_column(
        db.ForeignKey("notebooks.id"),
        nullable=False
    )

    summary_data: Mapped[dict] = mapped_column(
        db.JSON,
        nullable=False
    )

    upload_count: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False
    )

    generated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    notebook: Mapped["Notebook"] = db.relationship("Notebook", back_populates="summaries", lazy="raise_on_sql")
    upload_summary_relationships: Mapped[List["UploadSummaryRelationship"]] = db.relationship(
        back_populates="summary",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )