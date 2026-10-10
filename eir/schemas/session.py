from pydantic import BaseModel, Field

from eir.schemas.question import Question
from eir.schemas.answers import RecordedAnswer


class SessionCreate(BaseModel):
    patient_id: str

class SessionResponse(BaseModel):
    session_id: str
    patient_id: str
    current_question: Question
    completed: bool = False

class SessionState(BaseModel):
    session_id: str
    patient_id: str
    question_index: int = Field(default=0, ge=0)
    answers: list[RecordedAnswer] = Field(default_factory=list)
    completed: bool = False