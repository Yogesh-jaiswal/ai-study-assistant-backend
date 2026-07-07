from services.file_processors.extractors.docx_processor import DOCXProcessor


def test_extract_docx(monkeypatch, resource_dir):
    monkeypatch.setattr(
        DOCXProcessor,
        "_extract_images",
        lambda *_: []
    )

    processor = DOCXProcessor()

    text = processor.extract_text(
        resource_dir / "sample.docx"
    )

    assert "AI Study Assistant" in text
    assert "TXT | ✅ | Supported" in text