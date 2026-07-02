from typing import Literal
from dataclasses import dataclass

from .chunker import ChunkerFactory
from .cleaner.text_cleaner import TextCleaner
from .embeddings import EmbeddingFactory
from .extractors import TextExtractor

@dataclass
class ProcessedFile:
    cleaned_text: str
    chunks: list[str]
    embeddings: list[list[float]]

class FileProcessor:
    def __init__(
            self, 
            file_type: str,
            chunker_type: Literal["fixed", "sentence"] = "sentence",
            fake_embedder: bool = False, 
            test_mode: bool = False
    ):
        self.text_extractor = TextExtractor.get_processor(file_type, test_mode)
        self.text_cleaner = TextCleaner()
        self.chunker = ChunkerFactory.get_chunker(chunker_type)
        self.embedder = EmbeddingFactory.get_provider(fake_embedder)

    def process(self, file_path: str) -> tuple[str, list[str], list[list[float]]]:
        # Step 1: Extract text from the file
        extracted_text = self.text_extractor.extract_text(file_path)

        # Step 2: Clean the extracted text
        cleaned_text = self.text_cleaner.clean(extracted_text)

        # Step 3: Chunk the cleaned text
        chunks = self.chunker.chunk_text(cleaned_text)

        # Step 4: Generate embeddings for each chunk
        embeddings = self.embedder.embed_many(chunks)

        return ProcessedFile(
            cleaned_text=cleaned_text,
            chunks=chunks,
            embeddings=embeddings
        )