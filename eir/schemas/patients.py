from pydantic import BaseModel
class AddPatient(BaseModel):
    patient_id: str
    patient_name: str
    age: int
    gender: str
    language: str

