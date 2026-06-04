from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .upload import Upload
    from .summary import Summary

class UploadSummaryRelationship(db.Model):
    __tablename__ = "upload_summary_relationships"
    
    upload_id: Mapped[int] = mapped_column(db.ForeignKey("uploads.id"), primary_key=True)
    summary_id: Mapped[int] = mapped_column(db.ForeignKey("summaries.id"), primary_key=True)

    upload: Mapped["Upload"] = db.relationship("Upload", back_populates="upload_summary_relationships", lazy="raise_on_sql")
    summary: Mapped["Summary"] = db.relationship("Summary", back_populates="upload_summary_relationships", lazy="raise_on_sql")