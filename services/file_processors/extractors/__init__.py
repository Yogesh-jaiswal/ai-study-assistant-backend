import time
from models.enums import FileTypes

from .txt_processor import TextProcessor
from .md_processor import MarkdownProcessor
from .docx_processor import DOCXProcessor
from .pdf_processor import PDFProcessor
from .img_processor import ImageProcessor
from .csv_processor import CSVProcessor

from exceptions import UnsupportedFileTypeError

class TextExtractor:
    PROCESSORS = {
        FileTypes.TXT: TextProcessor,
        FileTypes.MARKDOWN: MarkdownProcessor,
        FileTypes.DOCX: DOCXProcessor,
        FileTypes.PDF: PDFProcessor,
        FileTypes.IMAGE: ImageProcessor,
        FileTypes.CSV: CSVProcessor
    }

    @staticmethod
    def get_processor(file_type: str, test_mode: bool = False):
        """Get the file processor according to file extension"""
        if test_mode:
            time.sleep(5) # Simulate a delay for testing purposes

        processor_class = TextExtractor.PROCESSORS.get(file_type)

        if not processor_class:
            raise UnsupportedFileTypeError(f"Unsupported file type {file_type}")
        
        return processor_class()