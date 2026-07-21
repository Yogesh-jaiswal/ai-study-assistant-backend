from pydantic import BaseModel, Field

class Option(BaseModel):
    label: str = Field(description="Display label such as A, B, C, D.")
    text: str = Field(description="Text shown to the student.")

class QuizQuestion(BaseModel):
    """Schema representing a single multiple-choice quiz question."""
    question: str = Field(..., min_length=10, description="The quiz question presented to the learner.")
    options: list[Option] = Field(..., min_length=4, description="Exactly four answer options for the question.")
    answer: str = Field(..., min_length=1, description="The label of the correct option (A, B, C or D).")
    explanation: str = Field(..., description="A concise explanation describing why the correct answer is correct.")

class QuizResponse(BaseModel):
    """Schema representing a generated quiz."""
    title: str = Field(..., description="A short descriptive title summarizing the quiz topic.")
    questions: list[QuizQuestion] = Field(..., description="The complete list of generated quiz questions.")