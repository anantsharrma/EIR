from fastapi import APIRouter
from eir.schemas.patients import AddPatient
router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/patients/")
def create_patient(patient: AddPatient):
    return AddPatient(
        patient_name=patient.patient_name,
        age=patient.age,
        gender=patient.gender,
        language=patient.language,
    )
