import logging
from pathlib import Path

from markdown_it import MarkdownIt

from .base_processor import BaseProcessor

from models.enums import DocumentBlockType

from services.file_processors.document.doc_representation import (
    DocumentBlock,
    DocumentRepresentation
)

logging.getLogger("markdown_it").setLevel(logging.WARNING)
logging.getLogger("markdown_it.rules_block").setLevel(logging.WARNING)

class MarkdownProcessor(BaseProcessor):
    """Markdown file processor"""

    def __init__(self):
        self.md = MarkdownIt()

    def extract(self, file_path: str | Path) -> DocumentRepresentation:
        with open(file_path, "r", encoding="utf-8") as file:
            tokens = self.md.parse(file.read())

        return DocumentRepresentation(
            blocks=self._extract_blocks(tokens),
        )

    @staticmethod
    def _extract_blocks(tokens) -> list[DocumentBlock]:
        blocks = []

        current_type = DocumentBlockType.PARAGRAPH
        in_list = False

        for token in tokens:
            match token.type:
                case "heading_open":
                    current_type = DocumentBlockType.HEADING

                case "paragraph_open":
                    current_type = (
                        DocumentBlockType.LIST
                        if in_list
                        else DocumentBlockType.PARAGRAPH
                    )

                case "bullet_list_open" | "ordered_list_open":
                    in_list = True

                case "bullet_list_close" | "ordered_list_close":
                    in_list = False

                case "inline":
                    text = token.content.strip()

                    if text:
                        blocks.append(
                            DocumentBlock(
                                type=current_type,
                                text=text,
                            )
                        )

                case "code_block" | "fence":
                    if token.content.strip():
                        blocks.append(
                            DocumentBlock(
                                type=DocumentBlockType.CODE,
                                text=token.content,
                            )
                        )

        return blocks