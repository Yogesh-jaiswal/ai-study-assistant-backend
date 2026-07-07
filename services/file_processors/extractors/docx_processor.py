from pathlib import Path
import tempfile
import zipfile

from PIL import Image
from docx import Document

from services.integrations.ocr_service import OCR

from .base_processor import BaseProcessor


class DOCXProcessor(BaseProcessor):
    """DOCX file processor"""

    def __init__(self):
        self.ocr = OCR()

    def extract_text(self, file_path: str | Path) -> str:
        document = Document(file_path)

        blocks = []

        # Paragraphs
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if text:
                blocks.append(text)

        # Tables
        for table in document.tables:
            rows = []

            for row in table.rows:
                cells = [
                    cell.text.strip()
                    for cell in row.cells
                ]

                rows.append(" | ".join(cells))

            blocks.append("\n".join(rows))

        # Images (OCR)
        blocks.extend(self._extract_images(file_path))

        return "\n\n".join(
            block
            for block in blocks
            if block.strip()
        )

    def _extract_images(self, file_path: str | Path):
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(file_path) as archive:
                archive.extractall(temp_dir)

            media_dir = (
                Path(temp_dir)
                / "word"
                / "media"
            )

            if not media_dir.exists():
                return []

            output = []

            for image_path in sorted(media_dir.iterdir()):
                if not image_path.is_file():
                    continue

                with Image.open(image_path) as img:
                    text = self.ocr.extract_text(img)

                if text:
                    output.append(text)

            return output