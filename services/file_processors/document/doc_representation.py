from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any

from models.enums import DocumentBlockType

DocumentBlockMetadata = dict[str, Any]

@dataclass
class DocumentBlock:
    type: DocumentBlockType
    text: str
    metadata: dict = field(default_factory=dict)

    def copy(self, **updates):
        return DocumentBlock(
            type=updates.get("type", self.type),
            text=updates.get("text", self.text),
            metadata={
                **deepcopy(self.metadata),
                **updates.get("metadata", {}),
            }
        )

@dataclass
class DocumentRepresentation:
    blocks: list[DocumentBlock]
    author: str | None = field(default=None)

    def to_text(self):
        return "\n\n".join(
            block.text
            for block in self.blocks
        )