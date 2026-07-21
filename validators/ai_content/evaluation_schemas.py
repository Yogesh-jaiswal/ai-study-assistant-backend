from pydantic import BaseModel, Field
from typing import List, Any
from datetime import datetime
from validators import UpdatedBaseModel

from models.enums import EvaluationTypes, ProcessingStatus

class EvaluateAttemptResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the celery background task")
    attempt_id: str = Field(..., description="Uniques identifier for the attempt")
    message: str = Field(..., description="Success message confirming user attempt evaluation")

class AttemptMetadata(BaseModel):
    id: str = Field(..., description="Unique identifier for the attempt")
    status: ProcessingStatus = Field(..., description="current processing status")
    total_marks: int | None = Field(..., description="Total marks of the user attempt this can be NULL for unevaluated attempts")
    obtained_marks: int | None = Field(..., description="Total obtained marks of the user attempt this can be NULL for unevaluated attempts")
    percentage: float | None = Field(..., description="Total obtained percenatage of the user attempt this can be NULL for unevaluated attempts")
    evaluation_type: EvaluationTypes = Field(..., description="Type of the evaluated user attempt")
    evaluated_at: datetime = Field(..., description="Timestamp of when the user attempt was evaluated")

class GetAttemptResponse(AttemptMetadata):
    evaluation: dict = Field(..., description="Content of the user attempt evaluation in JSON format")

class GetAllAttemptResponse(BaseModel):
    attempts: List[AttemptMetadata] = Field(..., description="List of all the user attempt from an ai content")

class Answer(BaseModel):
    question_id: str = Field(..., description="Unique Identifier of the question")
    answer: Any = Field(..., description="User's submitted answer")

class EvaluationRequest(UpdatedBaseModel):
    answers: List[Answer] = Field(..., description="All the user's submitted answer with question type")