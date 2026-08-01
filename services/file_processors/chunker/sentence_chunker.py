try:
    from nltk.tokenize import sent_tokenize
    sent_tokenize("test")
except LookupError:
    import nltk
    nltk.download("punkt_tab")
from .base_chunker import BaseChunker

class SentenceChunker(BaseChunker):
    """Divided the given text into sentence based separate chunks."""

    def __init__(self, max_sentences: int = 3, overlap_sentences: int = 1):
        if overlap_sentences >= max_sentences:
            raise ValueError(
                "overlap must be smaller than max sentences"
            )
        self.max_sentences = max_sentences
        self.overlap_sentences = overlap_sentences

    def chunk_text(self, text: str) -> list[str]:
        sentences = sent_tokenize(text)
        chunks = []
        start = 0

        while (start < len(sentences)):
            end = start + self.max_sentences
            chunk_text = "\n\n".join(sentences[start:end])
            chunks.append(chunk_text)

            start += (self.max_sentences - self.overlap_sentences)

        return chunks
