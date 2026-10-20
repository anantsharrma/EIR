from fastapi import APIRouter, HTTPException, Depends
from eir.schemas.session import SessionCreate, SessionResponse
from eir.schemas.answers import AnswerResponse,  GiveAnswer
from eir.services.session_service import (
    NoQuestionsConfiguredError,
    SessionAlreadyCompletedError,
    SessionNotFoundError,
    create_session as create_session_service,
    submit_answer as submit_answer_service,
    get_all_session as get_all_session_service,
    get_session as get_session_service,
)
from eir.services.error.session import (
SessionNotFoundError,
SessionAlreadyCompletedError,
NoQuestionsConfiguredError,
PatientHasNoSessionsErorr
)
from eir.services.error.patient import PatientNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from eir.db.sessions import get_db
router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(data: SessionCreate,
                         db: AsyncSession = Depends(get_db)) -> SessionResponse:
        try:
            return await create_session_service(data, db)
        except PatientNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except NoQuestionsConfiguredError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/{session_id}/answers", response_model=AnswerResponse)
async def submit_answer(
    session_id: str,
    data: GiveAnswer,
    db: AsyncSession = Depends(get_db)
) -> AnswerResponse:
    try:
        return await submit_answer_service(session_id, data, db)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SessionAlreadyCompletedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.get("/{patient_id}/sessions", status_code=200)
async def get_all_patient_sessions(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_all_session_service(patient_id, db)
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PatientHasNoSessionsErorr as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{patient_id}/{session_id}", status_code=200)
async def get_patient_session(patient_id: str, session_id: str, db: AsyncSession = Depends(get_db)):
        try:
            return await get_session_service(patient_id, session_id, db)
        except SessionNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc



