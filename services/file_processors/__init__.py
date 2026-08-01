from typing import Literal
from dataclasses import dataclass

from .chunker import ChunkerFactory
from .embeddings import EmbeddingFactory
from .extractors import DocumentProcessorFactory
from .document.document_chunker import DocumentChunker
from .document.doc_representation import DocumentRepresentation, DocumentBlock

@dataclass
class ProcessedChunk:
    block: DocumentBlock
    embedding: list[float]

    @property
    def text(self) -> str:
        return self.block.text

    @property
    def metadata(self) -> dict:
        return self.block.metadata

@dataclass
class ProcessedFile:
    document: DocumentRepresentation
    chunks: list[ProcessedChunk]

class FileProcessor:
    def __init__(
            self, 
            file_type: str,
            fake_embedder: bool = False, 
            test_mode: bool = False
    ):
        self.processor = DocumentProcessorFactory.get_processor(file_type, test_mode)
        self.embedder = EmbeddingFactory.get_provider(fake_embedder)
        self.chunker = DocumentChunker(self.embedder)

    def process(self, file_path: str) -> ProcessedFile:
        # Step 1: Extract blocks from the file
        document = self.processor.extract(file_path)

        # Step 2: Chunk the cleaned text
        chunks = self.chunker.split(document)

        # Step 3: Generate embeddings for each chunk
        embeddings = self.embedder.embed_many([chunk.text for chunk in chunks])

        processed_chunk = [
            ProcessedChunk(
                block=chunk,
                embedding=embedding
            ) for chunk, embedding in zip(chunks, embeddings)
        ]

        return ProcessedFile(
            document=document,
            chunks=processed_chunk
        )