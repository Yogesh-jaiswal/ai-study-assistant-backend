from dataclasses import dataclass
from models.enums import FileTypes

from services.file_processors.document.doc_representation import DocumentBlock

@dataclass(slots=True)
class RetrievedChunk:
    score: float
    chunk: DocumentBlock

    filename: str
    author: str | None
    source_type: FileTypes


@dataclass
class ContextBundle:
    chunks: list[RetrievedChunk]

    def to_text(self) -> str:
        return "\n\n---\n\n".join(
            chunk.chunk.text
            for chunk in self.chunks
        )

@dataclass(frozen=True)
class Citation:
    filename: str
    source_type: FileTypes
    author: str | None
    metadata: dict