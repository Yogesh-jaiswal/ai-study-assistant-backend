import logging

from models import Upload, DocumentChunk, ChunkEmbedding, Notebook
from exceptions import DatabaseError
from app.extensions import db
from configs import get_settings

# # Set up logging
logger = logging.getLogger(__name__)


def create_embedding(chunk_id: str, vector: list[float]) -> None:
    """
    Persist a embedding to the database.

    Raises:
        DatabaseError: If the transaction fails.
    """
    embedding = ChunkEmbedding(
        chunk_id=chunk_id,
        vector=vector
    )

    db.session.add(embedding)

    try:
        db.session.commit()
    except Exception:
        logger.exception("Failed creating embedding")
        db.session.rollback()
        raise DatabaseError("Failed to create embedding")

def bulk_create_embeddings(chunk_ids: list[str], vectors: list[list[float]]) -> None:
    """
    Persist multiple embeddings to the database at once.
    """
    embeddings = [
        ChunkEmbedding(
            chunk_id=chunk_id,
            vector=vector
        ) for chunk_id, vector in zip(chunk_ids, vectors)
    ]

    db.session.add_all(embeddings)

def get_embeddings_by_notebook(notebook_id: str, user_id: str) -> list[ChunkEmbedding]:
    """
    Retrieve all the embeddings of a certain notebook while enforcing user ownership.

    Returns:
        The embeddings if found owned by the user, otherwise empty list.
    """
    embeddings = (
        db.session.scalars(
            db.select(ChunkEmbedding)
            .join(DocumentChunk)
            .join(Upload)
            .join(Notebook)
            .where(
                Upload.notebook_id == notebook_id,
                Notebook.user_id == user_id,
            )
            .options(
                db.load_only(ChunkEmbedding.id, ChunkEmbedding.vector),
                db.joinedload(ChunkEmbedding.chunk).load_only(DocumentChunk.content),
            )
        )
        .all()
    )

    return embeddings

def get_embeddings_by_upload(upload_id: str, notebook_id: str, user_id: str) -> list[ChunkEmbedding]:
    """
    Retrieve all the embeddings of a certain upload while enforcing notebook ownership.

    Returns:
        The embeddings if found owned by the notebook, otherwise empty list.
    """
    embeddings = db.session.scalars(
        db.select(ChunkEmbedding)
        .join(DocumentChunk)
        .join(Upload)
        .join(Notebook)
        .where(
            DocumentChunk.upload_id == upload_id,
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    ).all()

    return embeddings

def get_embedding_by_chunk(chunk_id: str, upload_id: str, notebook_id: str, user_id: str) -> ChunkEmbedding | None:
    """
    Retrieve the embedding of a certain upload chunk while enforcing notebook ownership.

    Returns:
        The embedding if found owned by the notebook, otherwise none.
    """
    embeddings = db.session.scalar(
        db.select(ChunkEmbedding)
        .join(DocumentChunk)
        .join(Upload)
        .join(Notebook)
        .where(
            ChunkEmbedding.chunk_id == chunk_id,
            DocumentChunk.upload_id == upload_id,
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id
        )
    )

    return embeddings

def search_top_k_chunks(notebook_id: str, user_id: str, query_embedding: list[float], k: int = 5) -> list[tuple[float, str]] | None:
    """
    Retrieve top k chunks of a certain notebook based on given query embeddings.
    
    Returns:
        A list of dictionaries containing 'score' and 'content', 
        or None if PGVector is disabled.
    """
    settings = get_settings()

    if not settings.USE_PGVECTOR:
        return None
    
    # Injecting local precision window parameter onto Postgres query planner
    db.session.execute(db.text(f"SET local hnsw.ef_search = {settings.HNSW_EF_SEARCH};"))

    distance_expr = ChunkEmbedding.vector.cosine_distance(query_embedding)

    stmt = (
        db.select(
            DocumentChunk.content,
            distance_expr.label("distance")
        )
        .join(ChunkEmbedding.chunk)
        .join(Upload)
        .join(Notebook)
        .where(
            Upload.notebook_id == notebook_id,
            Notebook.user_id == user_id,
        )
        .order_by(distance_expr)
        .limit(k)
    )
    
    result = db.session.execute(stmt)

    final_result = []

    for row in result:
        score = max(0.0, 1.0 - row.distance)

        if score >= settings.MIN_SIMILARITY:
            final_result.append((round(score, 4), row.content))

    return final_result