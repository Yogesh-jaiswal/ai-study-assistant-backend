from services.file_processors.extractors.docx_processor import DOCXProcessor


def test_extract_docx(monkeypatch, resource_dir):
    """Test extracting text from a DOCX file."""
    monkeypatch.setattr(
        DOCXProcessor,
        "_extract_images",
        lambda *_: []
    )

    processor = DOCXProcessor()

    text = processor.extract(
        resource_dir / "sample.docx"
    ).to_text()

    assert "AI Study Assistant" in text
    assert "TXT | ✅ | Supported" in text