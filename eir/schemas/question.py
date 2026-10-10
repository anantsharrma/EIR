from enum import StrEnum
from pydantic import BaseModel, Field

class QuestionSection(StrEnum):
    CHIEF_COMPLAINT= "chief_complaint"
    DURATION = "duration"
    ASSOCIATED_SYMPTOMS = "associated_symptoms"

class Question(BaseModel):
    question_id: str
    section: QuestionSection
    prompt: str = Field(min_length=1)