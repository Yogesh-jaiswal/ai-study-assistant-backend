from dataclasses import dataclass

@dataclass
class FakeChunk:
    text: str
    start: float
    duration: float

class FakeYDL:
    """Fake YouTubeDL class for testing purposes."""
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def extract_info(self, *_args, **_kwargs):
        return {
            "id": "123",
            "title": "Test Video",
            "description": "Description",
            "uploader": "Test Channel",
        }


class FakeTranscript:
    """Fake Transcript class for testing purposes."""

    def fetch(self):
        return [
            FakeChunk("Hello World", 0.0, 1.5),
            FakeChunk("This is a fake extractor", 1.5, 2.0),
        ]


class FakeTranscriptList:
    """Fake TranscriptList class for testing purposes."""

    def find_transcript(self, *_):
        return FakeTranscript()


class FakeAPI:
    """Fake API class for testing purposes."""

    def list(self, *_):
        return FakeTranscriptList()