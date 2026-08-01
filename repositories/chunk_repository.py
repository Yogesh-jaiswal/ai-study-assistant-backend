import logging

from models import Upload, DocumentChunk, Notebook
from exceptions import DatabaseError
from app.extensions import db

# # Set up logging
logger = logging.getLogger(__name__)


def create_chunk(upload_id: str, chunk, idx: int) -> None:
    """
    Persist a chunk to the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    chunk = DocumentChunk(
        upload_id=upload_id,
        content=chunk.text,
        chunk_index=idx,
        block_type=chunk.block.type,
        chunk_metadata=chunk.metadata
    ) 

    db.session.add(chunk)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed creating chunk")
        db.session.rollback()
        raise DatabaseError("Failed to create chunk")

def bulk_create_chunks(upload_id: str, chunks: list) -> list[DocumentChunk]:
    """
    Persist multiple chunks to the database at once.
    """
    chunks = [
        DocumentChunk(
            upload_id=upload_id,
            content=chunk.text,
            chunk_index=idx,
            block_type=chunk.block.type,
            chunk_metadata=chunk.metadata
        ) for idx, chunk in enumerate(chunks)
    ]

    db.session.add_all(chunks)

    db.session.flush()

    return chunks

def get_chunks_by_upload(upload_id: str, notebook_id: str, user_id: str) -> list[DocumentChunk]:
    """
    Retrieve all the chunks of a certain upload while enforcing notebook ownership.

    Returns:
        The chunks if found owned by the user, otherwise empty list.
    """
    chunks = db.session.scalars(
        db.select(DocumentChunk)
        .join(Upload)
        .join(Notebook)
        .where(
            DocumentChunk.upload_id == upload_id,
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
        .order_by(DocumentChunk.chunk_index)
    ).all()

    return chunks