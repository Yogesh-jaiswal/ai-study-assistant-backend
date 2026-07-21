from services.file_processors.extractors.md_processor import MarkdownProcessor


def test_extract_markdown(resource_dir):
    processor = MarkdownProcessor()

    text = processor.extract_text(
        resource_dir / "sample.md"
    )

    assert isinstance(text, str)

    assert "AI Study Assistant" in text
    assert "Markdown parsing" in text
    assert "pytest" in text