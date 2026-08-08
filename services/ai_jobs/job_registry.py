"""
Module for registering AI jobs with their corresponding content types.
"""

from models.enums import AIContentTypes

from .summary_job import SummaryGenerationJob
from .quiz_job import QuizGenerationJob
from .flashcard_job import FlashcardGenerationJob
from .mind_map_job import MindMapGenerationJob
from .exam_job import ExamGenerationJob

AI_JOB_REGISTRY = {
    AIContentTypes.SUMMARY: SummaryGenerationJob(),
    AIContentTypes.QUIZ: QuizGenerationJob(),
    AIContentTypes.FLASHCARDS: FlashcardGenerationJob(),
    AIContentTypes.MIND_MAPS: MindMapGenerationJob(),
    AIContentTypes.EXAM: ExamGenerationJob()
}