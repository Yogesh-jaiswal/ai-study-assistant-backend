from pathlib import Path

from PIL import Image

from services.integrations.ocr_service import OCR

from .base_processor import BaseProcessor

class ImageProcessor(BaseProcessor):
    """Image file processor"""
    def __init__(self):
        self.ocr = OCR()
        
    def extract_text(self, file_path: str | Path) -> str:
        with Image.open(file_path) as img:
            return self.ocr.extract_text(img)