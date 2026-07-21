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