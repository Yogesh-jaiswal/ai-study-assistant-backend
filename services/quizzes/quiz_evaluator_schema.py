from pydantic import BaseModel, Field


class QuizQuestionEvaluation(BaseModel):
    question_id: str
    question: str
    obtained_marks: int
    maximum_marks: int
    status: str = Field(description="correct | incorrect | unanswered")
    user_answer: str | None
    correct_answer: str
    explanation: str


class QuizEvaluationResponse(BaseModel):
    questions: list[QuizQuestionEvaluation]