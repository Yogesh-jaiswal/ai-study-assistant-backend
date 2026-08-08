import pytest
from services.file_processors.chunker import FixedSizeChunker

chunker = FixedSizeChunker(
    chunk_size=10,
    overlap=0
)

def test_chunk_small_text():
    """Test chunking a small text that is smaller than the chunk size."""
    chunks = chunker.chunk_text("hello")

    assert chunks == ["hello"]

def test_chunk_exact_size():
    """Test chunking a text that is exactly the chunk size."""
    text = "abcdefghij"

    chunks = chunker.chunk_text(text)

    assert chunks == ["abcdefghij"]

def test_chunk_multiple_chunks():
    """Test chunking a text that results in multiple chunks."""
    text = "abcdefghij1234567890"

    chunks = chunker.chunk_text(text)

    assert chunks == [
        "abcdefghij",
        "1234567890"
    ]

def test_chunk_overlap():
    """Test chunking a text with overlap between chunks."""
    chunker = FixedSizeChunker(
        chunk_size=10,
        overlap=2
    )
    
    text = "abcdefghij1234567890"

    chunks = chunker.chunk_text(text)

    assert chunks == [
        "abcdefghij",
        "ij12345678",
        "7890"
    ]

def test_chunk_empty_text():
    """Test chunking an empty text."""
    chunks = chunker.chunk_text("")
    assert chunks == []

def test_invalid_overlap():
    """Test that initializing the chunker with an invalid overlap raises a ValueError."""
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            overlap=100
        )

def test_overlap_larger_than_chunk():
    """Test that initializing the chunker with an overlap larger than the chunk size raises a ValueError."""
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            overlap=200
        )