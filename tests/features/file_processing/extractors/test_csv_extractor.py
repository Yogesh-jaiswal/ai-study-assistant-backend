from services.file_processors.extractors.csv_processor import CSVProcessor


def test_extract_csv(resource_dir):
    """Test extracting text from a CSV file."""
    processor = CSVProcessor()

    text = processor.extract(
        resource_dir / "sample.csv"
    ).to_text()

    assert "Student ID" in text
    assert "Yogesh Jaiswal" in text
    assert "|" in text