import time
from .base_processor import BaseProcessor

class TextProcessor(BaseProcessor):
    """Text file processor"""

    def extract_text(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
        
class SlowTextProcessor(TextProcessor):
    """Special slow processor for testing purposes."""

    def extract_text(self, file_path):
        time.sleep(5)
        return super().extract_text(file_path)