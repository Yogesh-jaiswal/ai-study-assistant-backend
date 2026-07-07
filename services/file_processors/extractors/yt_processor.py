from uuid import UUID

from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from .base_processor import BaseProcessor

class YouTubeProcessor(BaseProcessor):
    def __init__(self):
        self.ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

    def extract_text(self, url: str) -> str:
        """Extract text from the given youtube video URL"""
        sections = []

        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_id = info["id"]
        title = info.get("title", "")
        description = info.get("description", "")
        transcript = self._extract_transcript(video_id)

        if title: sections.append(f"Title:\n{title}")
        
        if description: sections.append(f"Description:\n{description}")

        sections.append(f"Transcript:\n{transcript}")

        return "\n\n".join(sections)
    
    @staticmethod
    def _extract_transcript(video_id: str | UUID) -> str:
        api = YouTubeTranscriptApi()

        transcript_list = api.list(video_id)

        try:
            transcript = transcript_list.find_transcript(["en"])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript(["en"])
            except NoTranscriptFound:
                transcript = next(iter(transcript_list))
        data = transcript.fetch()

        transcript_text = " ".join(chunk.text.strip() for chunk in data)

        if not transcript_text.strip():
            raise ValueError("Transcript is empty")

        return transcript_text