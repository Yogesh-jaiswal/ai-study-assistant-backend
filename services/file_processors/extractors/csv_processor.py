import csv
from pathlib import Path

from .base_processor import BaseProcessor

from services.file_processors.document.doc_representation import (
    DocumentBlock,
    DocumentRepresentation
)

from models.enums import DocumentBlockType

class CSVProcessor(BaseProcessor):
    """CSV file processor"""

    BLOCK_SIZE = 50

    def extract(self, file_path: str | Path) -> DocumentRepresentation:
        blocks = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            chunk: list[str] = []
            start_row = 1
            current_row = 0

            for row in reader:
                if not row:
                    continue

                current_row += 1

                chunk.append(
                    " | ".join(cell.strip() for cell in row)
                )

                if len(chunk) == self.BLOCK_SIZE:
                    blocks.append(
                        DocumentBlock(
                            type=DocumentBlockType.TABLE,
                            text="\n".join(chunk),
                            metadata={
                                "row_range": f"{start_row}-{current_row}"
                            },
                        )
                    )
                    chunk.clear()
                    start_row = current_row + 1

            # Flush any remaining rows
            if chunk:
                blocks.append(
                    DocumentBlock(
                        type=DocumentBlockType.TABLE,
                        text="\n".join(chunk),
                        metadata={
                            "row_range": f"{start_row}-{current_row}"
                        },
                    )
                )

        return DocumentRepresentation(
            blocks=blocks,
        )