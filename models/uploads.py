from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .notebook import Notebook
    from .upload_summary_relationship import UploadSummaryRelationship

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileTypes(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    XLSX = "xlsx"
    PPTX = "pptx"
    MARKDOWN = "md"

class Upload(db.Model):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    notebook_id: Mapped[int] = mapped_column(
        db.ForeignKey("notebooks.id"),
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False
    )

    source_type: Mapped[FileTypes] = mapped_column(
        db.Enum(FileTypes),
        nullable=False
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        db.Enum(ProcessingStatus),
        nullable=False,
        default=ProcessingStatus.PENDING,
        server_default=ProcessingStatus.PENDING.name
    )

    raw_text: Mapped[str | None] = mapped_column(
        db.Text,
        nullable=True
    )

    error_message: Mapped[str | None] = mapped_column(
        db.Text,
        nullable=True
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    notebook: Mapped["Notebook"] = db.relationship("Notebook", back_populates="upload", lazy="raise_on_sql")
    upload_summary_relationship: Mapped[List["UploadSummaryRelationship"]] = db.relationship(
        back_populates="upload",
        cascade="all, delete-orphan",
        lazy="raise_on_sql"
    )