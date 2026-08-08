from services.file_processors.extractors.pdf_processor import PDFProcessor
from services.integrations.ocr_service import OCR


def test_extract_pdf(monkeypatch, resource_dir):
    """Test extracting text from a PDF file."""
    monkeypatch.setattr(
        OCR,
        "extract_text",
        lambda *_: "Mock OCR"
    )

    processor = PDFProcessor()

    text = processor.extract(
        resource_dir / "sample.pdf"
    ).to_text()

    assert "AI Study Assistant" in text