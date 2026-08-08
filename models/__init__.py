"""
Database models for the AI Study Assistant backend.

Defines the SQLAlchemy models representing users, notebooks,
uploads, generated AI content, attempts, exam blueprints,
and related persistent entities.
"""

from .user import User
from .notebook import Notebook
from .ai_content import AIContent
from .upload import Upload
from .upload_ai_content_relationship import UploadAIContentRelationship
from .refresh_token import RefreshToken
from .document_chunk import DocumentChunk
from .chunk_embeddings import ChunkEmbedding
from .exam_blueprint import ExamBlueprint
from .user_attempt import UserAttempt

# Define the __all__ variable to specify the public API of the models package
__all__ = [
    "User",
    "Notebook",
    "AIContent",
    "Upload",
    "UploadAIContentRelationship",
    "RefreshToken",
    "DocumentChunk",
    "ChunkEmbedding",
    "ExamBlueprint",
    "UserAttempt"
]