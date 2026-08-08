from pydantic import BaseModel, Field


class QuizQuestionEvaluation(BaseModel):
    """Represents the evaluation of a single question in a quiz, including details about the question, the user's answer, and the correct answer."""
    question_id: str
    question: str
    obtained_marks: int
    maximum_marks: int
    status: str = Field(description="correct | incorrect | unanswered")
    user_answer: str | None
    correct_answer: str
    explanation: str


class QuizEvaluationResponse(BaseModel):
    """Represents the overall evaluation of a quiz, including feedback and evaluations for each question."""
    questions: list[QuizQuestionEvaluation]