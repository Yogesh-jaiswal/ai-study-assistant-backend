from pydantic import BaseModel

class QuestionEvaluation(BaseModel):
    question_id: str
    obtained_marks: float
    feedback: str

class SectionEvaluation(BaseModel):
    section_name: str
    questions: list[QuestionEvaluation]

class ExamEvaluationResponse(BaseModel):
    overall_feedback: str
    sections: list[SectionEvaluation]