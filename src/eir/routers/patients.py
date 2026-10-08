from fastapi import APIRouter
from src.eir.schemas.patients import addPatient
router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/patients/")
def create_patient(patient: addPatient):
    return addPatient(
        patient_name=patient.patient_name,
        age=patient.age,
        gender=patient.gender,
        language=patient.language,
    )
