from services.file_processors.extractors import yt_processor

from tests.fakes.fake_youtube_extractor import FakeYDL, FakeAPI


def test_extract_youtube(monkeypatch):

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

    text = processor.extract_text(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # <- If you have find it don't open it
    )

    assert "Test Video" in text
    assert "Description" in text
    assert "Hello World" in text