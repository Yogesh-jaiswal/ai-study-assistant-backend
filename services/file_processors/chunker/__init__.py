from typing import Literal
from .fixed_chunker import FixedSizeChunker
from .sentence_chunker import SentenceChunker
from .token_chunker import TokenChunker

class ChunkerFactory:

    def get_chunker(type: Literal["fixed", "sentence", "token"] = "fixed"):
        match type:
            case "fixed":
                return FixedSizeChunker()
            case "sentence":
                return SentenceChunker()
            case "token":
                return TokenChunker()
            case _:
                raise ValueError("Unknown chunker type")