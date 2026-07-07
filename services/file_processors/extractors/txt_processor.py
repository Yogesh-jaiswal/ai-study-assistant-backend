from pathlib import Path

from .base_processor import BaseProcessor

class TextProcessor(BaseProcessor):
    """Text file processor"""

    def extract_text(self, file_path: str | Path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()