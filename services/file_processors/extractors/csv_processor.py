import csv
from pathlib import Path

from .base_processor import BaseProcessor

class CSVProcessor(BaseProcessor):
    """CSV file processor"""

    def extract_text(self, file_path: str | Path):
        rows = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if not row:
                    continue

                rows.append(
                    " | ".join(
                        cell.strip() 
                        for cell in row
                    )
                )

        return "\n".join(rows)