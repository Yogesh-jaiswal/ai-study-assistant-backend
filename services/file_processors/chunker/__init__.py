from typing import Literal
from .fixed_chunker import FixedSizeChunker
from .sentence_chunker import SentenceChunker

class ChunkerFactory:

    def get_chunker(type: Literal["fixed", "sentence"] = "fixed"):
        match type:
            case "fixed":
                return FixedSizeChunker()
            case "sentence":
                return SentenceChunker()
            case _:
                raise ValueError("Unknown chunker type")