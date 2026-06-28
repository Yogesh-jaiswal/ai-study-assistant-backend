from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract text from the file using given file path"""
        pass