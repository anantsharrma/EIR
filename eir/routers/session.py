
from fastapi import APIRouter, HTTPException
from eir.schemas.session import SessionCreate, SessionResponse
from eir.schemas.answers import AnswerResponse,  GiveAnswer
from eir.services.session_service import (
    NoQuestionsConfiguredError,
    SessionAlreadyCompletedError,
    SessionNotFoundError,
    create_session as create_session_service,
    submit_answer as submit_answer_service,
)
router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(data: SessionCreate) -> SessionResponse:
        try:
            return create_session_service(data)
        except NoQuestionsConfiguredError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/{session_id}/answers", response_model=AnswerResponse)
async def submit_answer(
    session_id: str,
    data: GiveAnswer
) -> AnswerResponse:
    try:
        return submit_answer_service(session_id, data)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SessionAlreadyCompletedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc