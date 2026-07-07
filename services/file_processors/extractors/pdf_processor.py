from pathlib import Path

import pymupdf
from PIL import Image

from services.integrations.ocr_service import OCR

from .base_processor import BaseProcessor

MIN_TEXT_THRESHOLD = 120
MIN_IMAGE_COVERAGE = 0.7
OCR_DPI = 250

class PDFProcessor(BaseProcessor):
    """PDF file processor"""
    def __init__(self):
        self.ocr = OCR()
        
    def extract_text(self, file_path: str | Path) -> str:
        output = []
        seen = set()

        with pymupdf.open(file_path) as doc:
            for page in doc:
                blocks = self._process_page(page)

                for block in blocks:
                    block = block.strip()
                    if block and block not in seen:
                        seen.add(block)
                        output.append(block)

        return "\n\n".join(output)
    
    def _process_page(self, page) -> list[str]:
        page_dict = page.get_text("dict")

        text_length = self._text_length(page_dict)

        if text_length >= MIN_TEXT_THRESHOLD:
            return self._extract_text(page, page_dict)
        
        return self._extract_ocr(page, page_dict)
    
    @staticmethod
    def _text_length(page_dict) -> int:
        total = 0

        for block in page_dict["blocks"]:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    total += len(span["text"])

                    if total >= MIN_TEXT_THRESHOLD:
                        return total
                    
        return total
    
    def _extract_text(self, page, page_dict) -> list[str]:
        tables = page.find_tables().tables
        table_rects = [pymupdf.Rect(table.bbox) for table in tables]

        output = []

        output.extend(self._extract_tables(tables))

        for block in page_dict["blocks"]:

            if block["type"] != 0:
                continue

            rect = pymupdf.Rect(block["bbox"])

            if any(rect.intersects(r) for r in table_rects):
                continue

            text = "".join(
                span["text"]
                for line in block["lines"]
                for span in line["spans"]
            ).strip()

            if text:
                output.append(text)

        return output
    
    def _extract_tables(self, tables) -> list[str]:
        output = []

        for table in tables:
            rows = table.extract()

            text = "\n".join(
                " | ".join(
                    (cell or "").strip() 
                    for cell in row
                ) 
                for row in rows
            ).strip()

            if text:
                output.append(text)

        return output
    
    def _extract_ocr(self, page, page_dict) -> list[str]:
        page_rect = page.rect
        page_area = page_rect.width * page_rect.height

        largest = None
        largest_area = 0

        for block in page_dict["blocks"]:
            if block["type"] != 1:
                continue

            rect = pymupdf.Rect(block["bbox"])
            area = rect.width * rect.height

            if area > largest_area:
                largest = rect
                largest_area = area

        if largest and largest_area / page_area >= MIN_IMAGE_COVERAGE:
            pix = page.get_pixmap(
                clip=largest,
                dpi=OCR_DPI
            )
        else:
            pix = page.get_pixmap(
                dpi=OCR_DPI
            )

        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(
            mode,
            (pix.width, pix.height),
            pix.samples
        )
        
        text = self.ocr.extract_text(img)

        return [text] if text else []