from sklearn.metrics.pairwise import cosine_similarity

from repositories.embedding_repository import get_embeddings_by_notebook
from configs import get_settings

from models import DocumentChunk, Upload

def top_k_search(notebook_id: str, user_id: str, query_embedding: list[float], k: int = 5) -> list[tuple[float, DocumentChunk, Upload]]:
    """
    Search query in stored embeddings and return top k result
    """
    embeddings = get_embeddings_by_notebook(notebook_id, user_id)

    results = []

    for embedding in embeddings:
        score = cosine_similarity(
            [query_embedding],
            [embedding.vector]
        )[0][0]

        if score >= get_settings().MIN_SIMILARITY:
            results.append(
                (
                    round(score, 4),
                    embedding.chunk,
                    embedding.chunk.upload,
                )
            )

    results.sort(reverse=True)

    return results[:k]