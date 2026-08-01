from uuid import UUID

from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from .base_processor import BaseProcessor

from models.enums import DocumentBlockType

from services.file_processors.document.doc_representation import (
    DocumentBlock,
    DocumentRepresentation
)

class YouTubeProcessor(BaseProcessor):
    def __init__(self):
        self.ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

    def extract(self, url: str) -> DocumentRepresentation:
        """Extract text from the given youtube video URL"""
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_id = info["id"]
        
        description = info.get("description", "")
        description_block = DocumentBlock(
            type = DocumentBlockType.DESCRIPTION,
            text = description
        )
        
        transcript_blocks = self._extract_transcript(video_id)

        return DocumentRepresentation(
            author=info.get("uploader"),
            blocks=[
                description_block,
                *transcript_blocks,
            ],
        )
    
    @staticmethod
    def _extract_transcript(video_id: str | UUID) -> list[DocumentBlock]:
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

        blocks = []

        for chunk in data:
            text = chunk.text.strip()
            if not text:
                continue

            start = chunk.start
            end = start + chunk.duration

            blocks.append(
                DocumentBlock(
                    type=DocumentBlockType.TRANSCRIPT,
                    text=text,
                    metadata={
                        "start": start,
                        "end": end
                    },
                )
            )

        if not blocks:
            raise ValueError("Transcript is empty")

        return blocks