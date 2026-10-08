from pydantic import BaseModel
class addPatient(BaseModel):
    patient_name: str
    age: int
    gender: str
    language: str

