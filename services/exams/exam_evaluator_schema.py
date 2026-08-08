from pydantic import BaseModel

class QuestionEvaluation(BaseModel):
    """Represents the evaluation of a single question in an exam."""
    question_id: str
    obtained_marks: float
    feedback: str

class SectionEvaluation(BaseModel):
    """Represents the evaluation of a section in an exam, containing multiple questions."""
    section_name: str
    questions: list[QuestionEvaluation]

class ExamEvaluationResponse(BaseModel):
    """Represents the overall evaluation of an exam, including feedback and section evaluations."""
    overall_feedback: str
    sections: list[SectionEvaluation]