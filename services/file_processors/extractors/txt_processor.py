from pathlib import Path

from .base_processor import BaseProcessor

from models.enums import DocumentBlockType

from services.file_processors.document.doc_representation import (
    DocumentBlock,
    DocumentRepresentation
)

class TextProcessor(BaseProcessor):
    """Text file processor"""

    def extract(self, file_path: str | Path) -> DocumentRepresentation:
        with open(file_path, "r", encoding="utf-8") as file:
            return DocumentRepresentation(
                blocks=[
                    DocumentBlock(
                        type=DocumentBlockType.PARAGRAPH,
                        text=file.read()
                    )
                ]
            )