from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eir.models.patients import Patient as PatientModel
from eir.schemas.patients import PatientCreate, PatientResponse
from eir.services.questions import QUESTIONS

async def create_patient(
        data: PatientCreate,
        db: AsyncSession) -> PatientResponse:
    Patient = PatientModel(
        patient_id=str(uuid4()),
        patient_name=data.patient_name,
        age=data.age,
        gender=data.gender,
        language=data.language,
    )
    db.add(Patient)
    await db.commit()
    await db.refresh(Patient)
    return PatientResponse(
        patient_id=str(Patient.patient_id),
        patient_name=Patient.patient_name,
        age=Patient.age,
        gender=Patient.gender,
        language=Patient.language,
    )

