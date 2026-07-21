from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .upload import Upload
    from .ai_content import AIContent

class UploadAIContentRelationship(db.Model):
    __tablename__ = "upload_ai_content_relationships"
    
    upload_id: Mapped[str] = mapped_column(db.ForeignKey("uploads.id"), primary_key=True)
    ai_content_id: Mapped[str] = mapped_column(db.ForeignKey("ai_contents.id"), primary_key=True)

    upload: Mapped["Upload"] = db.relationship("Upload", back_populates="upload_ai_content_relationships", lazy="raise_on_sql")
    ai_content: Mapped["AIContent"] = db.relationship("AIContent", back_populates="upload_ai_content_relationships", lazy="raise_on_sql")