from dataclasses import dataclass

@dataclass
class FakeChunk:
    text: str
    start: float
    duration: float

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
            "uploader": "Test Channel",
        }


class FakeTranscript:

    def fetch(self):
        return [
            FakeChunk("Hello World", 0.0, 1.5),
            FakeChunk("This is a fake extractor", 1.5, 2.0),
        ]


class FakeTranscriptList:

    def find_transcript(self, *_):
        return FakeTranscript()


class FakeAPI:

    def list(self, *_):
        return FakeTranscriptList()