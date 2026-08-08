from services.file_processors.extractors import yt_processor

from tests.fakes.fake_youtube_extractor import FakeYDL, FakeAPI


def test_extract_youtube(monkeypatch):
    """Test extracting text from a YouTube video."""

    monkeypatch.setattr(
        yt_processor,
        "YoutubeDL",
        lambda *_: FakeYDL(),
    )

    monkeypatch.setattr(
        yt_processor,
        "YouTubeTranscriptApi",
        lambda: FakeAPI(),
    )

    processor = yt_processor.YouTubeProcessor()

    text = processor.extract(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # <- If you have find it don't open it
    ).to_text()
    
    assert "Description" in text
    assert "Hello World" in text