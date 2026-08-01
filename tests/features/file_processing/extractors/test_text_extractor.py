from services.file_processors.extractors.txt_processor import TextProcessor


def test_extract_text(resource_dir):
    processor = TextProcessor()

    text = processor.extract(
        resource_dir / "sample.txt"
    ).to_text()

    assert isinstance(text, str)
    assert len(text) > 100

    assert "AI Study Assistant" in text
    assert "Markdown parsing" in text