from services.file_processors.extractors import yt_processor


class FakeYDL:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def extract_info(self, *_args, **_kwargs):
        return {
            "id": "123",
            "title": "Test Video",
            "description": "Description",
        }


class FakeTranscript:

    def fetch(self):
        return [
            type("Chunk", (), {"text": "Hello"})(),
            type("Chunk", (), {"text": "World"})(),
        ]


class FakeTranscriptList:

    def find_transcript(self, *_):
        return FakeTranscript()


class FakeAPI:

    def list(self, *_):
        return FakeTranscriptList()


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