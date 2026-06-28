import uuid
import json
from datetime import datetime
from sqlalchemy import (
    func,
    Index,
    TypeDecorator,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from configs import get_settings

from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .document_chunk import DocumentChunk

class CompatibleVector(TypeDecorator):
    """
    A vector wrapper that uses pgvector on Postgres, 
    but safely falls back to a JSON text blob on SQLite.
    """
    impl = Text
    cache_ok = True

    def __init__(self, dimensions):
        super().__init__()
        self.dimensions = dimensions

    def load_dialect_impl(self, dialect):
        # If the active engine is PostgreSQL, use pgvector otherwise test storage
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(Vector(self.dimensions))
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if dialect.name != 'postgresql' and value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if dialect.name != 'postgresql' and value is not None:
            return json.loads(value)
        return value


class ChunkEmbedding(db.Model):
    __tablename__ = "chunk_embeddings"

    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    chunk_id: Mapped[str] = mapped_column(
        db.ForeignKey("document_chunks.id"),
        nullable=False
    )

    vector: Mapped[str | list[float]] = mapped_column(
        CompatibleVector(384),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    chunk: Mapped["DocumentChunk"] = db.relationship("DocumentChunk", back_populates="embedding", lazy="raise_on_sql")