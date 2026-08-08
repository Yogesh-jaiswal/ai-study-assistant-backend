from services.file_processors.extractors.img_processor import ImageProcessor
from services.integrations.ocr_service import OCR


def test_extract_image(monkeypatch, resource_dir):
    """Test extracting text from a image file."""
    monkeypatch.setattr(
        OCR,
        "extract_text",
        lambda *_: "Mock OCR"
    )

    processor = ImageProcessor()

    text = processor.extract(
        resource_dir / "sample.jpg"
    ).to_text()

    assert text == "Mock OCR"