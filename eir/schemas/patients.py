from pydantic import BaseModel
class PatientCreate(BaseModel):
    patient_name: str
    age: int
    gender: str
    language: str
class PatientResponse(BaseModel):
    patient_id: str
    patient_name: str
    age: int
    gender: str
    language: str
