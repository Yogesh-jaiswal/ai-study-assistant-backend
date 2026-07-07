from services.file_processors.extractors.csv_processor import CSVProcessor


def test_extract_csv(resource_dir):
    processor = CSVProcessor()

    text = processor.extract_text(
        resource_dir / "sample.csv"
    )

    assert "Student ID" in text
    assert "Yogesh Jaiswal" in text
    assert "|" in text