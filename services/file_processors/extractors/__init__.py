"""
Document extraction services.

Provides processors for extracting usable content from
supported file and external content sources.
"""

import time
from models.enums import FileTypes

from .txt_processor import TextProcessor
from .md_processor import MarkdownProcessor
from .docx_processor import DOCXProcessor
from .pdf_processor import PDFProcessor
from .img_processor import ImageProcessor
from .csv_processor import CSVProcessor
from .yt_processor import YouTubeProcessor

from exceptions import UnsupportedFileTypeError

class DocumentProcessorFactory:
    """A factory class to create different types of document processors based on the specified file type."""
    PROCESSORS = {
        FileTypes.TXT: TextProcessor,
        FileTypes.MARKDOWN: MarkdownProcessor,
        FileTypes.DOCX: DOCXProcessor,
        FileTypes.PDF: PDFProcessor,
        FileTypes.IMAGE: ImageProcessor,
        FileTypes.CSV: CSVProcessor,
        FileTypes.YOUTUBE: YouTubeProcessor
    }

    @staticmethod
    def get_processor(file_type: str, test_mode: bool = False):
        """Get the file processor according to file extension"""
        if test_mode:
            time.sleep(0) # Simulate a delay for testing purposes

        processor_class = DocumentProcessorFactory.PROCESSORS.get(file_type)

        if not processor_class:
            raise UnsupportedFileTypeError(f"Unsupported file type {file_type}")
        
        return processor_class()