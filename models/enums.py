from enum import Enum

class UploadPurpose(str, Enum):
    NOTES = "notes"
    REFERENCE = "reference"

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileTypes(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    MARKDOWN = "md"
    IMAGE = "img"
    YOUTUBE = "yt"

class AIContentTypes(str, Enum):
    SUMMARY = "summary"
    QUIZ = "quiz"
    FLASHCARDS = "flashcards"
    MIND_MAPS = "mind_maps"
    EXAM = "exam"

class EvaluationTypes(str, Enum):
    QUIZ = "quiz"
    EXAM = "exam"

class DocumentBlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    TABLE = "table"
    OCR = "ocr"
    CODE = "code"
    LIST = "list"
    TRANSCRIPT = "transcript"
    DESCRIPTION = "description"