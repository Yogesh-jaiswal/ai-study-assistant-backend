from models.enums import FileTypes

from .text_processor import TextProcessor, SlowTextProcessor

from exceptions import UnsupportedFileTypeError

class FileProcessor:
    PROCESSORS = {
        FileTypes.TXT: TextProcessor
    }

    @staticmethod
    def get_processor(file_type: str, test_mode: bool = False):
        """Get the file processor according to file extension"""
        if test_mode:
            return SlowTextProcessor()

        processor_class = FileProcessor.PROCESSORS.get(file_type)

        if not processor_class:
            raise UnsupportedFileTypeError(f"Unsupported file type {file_type}")
        
        return processor_class()