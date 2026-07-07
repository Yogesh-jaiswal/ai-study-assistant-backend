from pathlib import Path

from markdown_it import MarkdownIt

from .base_processor import BaseProcessor

class MarkdownProcessor(BaseProcessor):
    """Markdown file processor"""
    def __init__(self):
        self.md = MarkdownIt()
        
    def extract_text(self, file_path: str | Path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            tokens = self.md.parse(file.read())
            return self._extract_text_from_tokens(tokens)

    @staticmethod
    def _extract_text_from_tokens(tokens):
        lines = []
        for token in tokens:
            if token.type == "inline" and token.content.strip():
                lines.append(token.content)

            elif token.type in (
                "paragraph_close",
                "heading_close",
                "blockquote_close",
                "bullet_list_close",
                "ordered_list_close"
            ):
                lines.append("")

            elif token.type in ("code_block", "fence"):
                lines.append(token.content)
                lines.append("")
                
        return "\n".join(lines).strip()