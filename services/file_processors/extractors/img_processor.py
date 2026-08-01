from pathlib import Path

from PIL import Image

from services.integrations.ocr_service import OCR

from .base_processor import BaseProcessor

from models.enums import DocumentBlockType

from services.file_processors.document.doc_representation import (
    DocumentBlock,
    DocumentRepresentation
)

class ImageProcessor(BaseProcessor):
    """Image file processor"""
    def __init__(self):
        self.ocr = OCR()
        
    def extract(self, file_path: str | Path) -> DocumentRepresentation:
        with Image.open(file_path) as img:
            text = self.ocr.extract_text(img)
            blocks = []

            if text.strip():
                blocks.append(
                    DocumentBlock(
                        type=DocumentBlockType.OCR,
                        text=text
                    )
                )
                
            return DocumentRepresentation(
                blocks=blocks
            )