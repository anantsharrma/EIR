from pydantic import BaseModel

class SessionCreate(BaseModel):
    patient_id: str

class SessionResponse(BaseModel):
    patient_id: str
    session_id: str
    current_section: str
    current_question: str