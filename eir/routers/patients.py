from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from eir.services.session_service import PatientNotFoundError
from eir.db.sessions import get_db
from eir.schemas.session import SessionCreate, SessionResponse
from eir.services.patient_service import create_patient as create_patient_service
from eir.schemas.patients import AddPatient
router = APIRouter(prefix="/patient", tags=["Patients"])
from sqlalchemy import select
from eir.models.patients import Patient
from sqlalchemy.orm import selectinload
@router.post("/register", response_model=AddPatient, status_code=201)
async def create_patient(
    data: AddPatient,
    db: AsyncSession = Depends(get_db),
) -> AddPatient:
        return await create_patient_service(data, db)

@router.get("/all_patients", status_code=200)
async def get_all_patients(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Patient))
        patients = result.scalars().all()
        return patients

@router.get("/patient/{patient_id}", status_code=200)
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db)):
        try:
                result = await db.execute(select(Patient).options(selectinload(Patient.sessions)).where(Patient.patient_id == patient_id))
                patient = result.scalar_one_or_none()
                return patient
        except PatientNotFoundError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

