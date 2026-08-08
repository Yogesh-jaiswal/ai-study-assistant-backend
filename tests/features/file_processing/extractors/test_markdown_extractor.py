from services.file_processors.extractors.md_processor import MarkdownProcessor


def test_extract_markdown(resource_dir):
    """Test extracting text from a Markdown file."""
    processor = MarkdownProcessor()

    text = processor.extract(
        resource_dir / "sample.md"
    ).to_text()

    assert isinstance(text, str)

    assert "AI Study Assistant" in text
    assert "Markdown parsing" in text
    assert "pytest" in text