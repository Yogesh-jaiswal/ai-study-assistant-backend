import pytest
from services.chunker import FixedSizeChunker

chunker = FixedSizeChunker(
    chunk_size=10,
    overlap=0
)

def test_chunk_small_text():
    chunks = chunker.chunk("hello")

    assert chunks == ["hello"]

def test_chunk_exact_size():
    text = "abcdefghij"

    chunks = chunker.chunk(text)

    assert chunks == ["abcdefghij"]

def test_chunk_multiple_chunks():
    text = "abcdefghij1234567890"

    chunks = chunker.chunk(text)

    assert chunks == [
        "abcdefghij",
        "1234567890"
    ]

def test_chunk_overlap():
    text = "abcdefghij1234567890"

    chunks = chunker.chunk(text)

    assert chunks == [
        "abcdefghij",
        "ij12345678",
        "7890"
    ]

def test_chunk_empty_text():
    chunks = chunker.chunk("")

    assert chunks == []

def test_invalid_overlap():
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            overlap=100
        )

def test_overlap_larger_than_chunk():
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            overlap=200
        )