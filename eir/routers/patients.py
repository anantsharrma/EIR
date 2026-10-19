from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from eir.db.sessions import get_db
from eir.schemas.session import SessionCreate, SessionResponse
from eir.services.patient_service import create_patient as create_patient_service
from eir.schemas.patients import AddPatient
router = APIRouter(prefix="/patient", tags=["Patients"])


@router.post("", response_model=AddPatient, status_code=201)
async def create_patient(
    data: AddPatient,
    db: AsyncSession = Depends(get_db),
) -> AddPatient:
        return await create_patient_service(data, db)