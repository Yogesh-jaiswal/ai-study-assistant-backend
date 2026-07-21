from pydantic import BaseModel, Field

class Flashcard(BaseModel):
    """Schema representing a single flashcard content"""
    front: str = Field(..., description="The front should contain a concise question, keyword, or cue.")
    back: str = Field(..., description="The back should contain a short, accurate answer.")

class FlashcardResponse(BaseModel):
    """Schema representing a generated quiz."""
    title: str = Field(..., description="A short descriptive title summarizing the flashcards topic.")
    flashcards: list[Flashcard] = Field(..., description="The complete list of generated flashcards.")