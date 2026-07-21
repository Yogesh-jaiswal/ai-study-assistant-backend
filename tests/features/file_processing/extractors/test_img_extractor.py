from services.file_processors.extractors.img_processor import ImageProcessor
from services.integrations.ocr_service import OCR


def test_extract_image(monkeypatch, resource_dir):
    monkeypatch.setattr(
        OCR,
        "extract_text",
        lambda *_: "Mock OCR"
    )

    processor = ImageProcessor()

    text = processor.extract_text(
        resource_dir / "sample.jpg"
    )

    assert text == "Mock OCR"