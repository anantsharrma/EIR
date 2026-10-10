from pydantic import BaseModel, Field
from eir.schemas.question import Question
class GiveAnswer(BaseModel):
    answer: str = Field(min_length=1)

class RecordedAnswer(BaseModel):
    question_id: str
    question_text: str
    answer: str

class AnswerResponse(BaseModel):
    session_id: str
    answer: str
    next_question: Question | None = None
    recorded: bool
    completed: bool

