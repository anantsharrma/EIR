from uuid import uuid4
from src.eir.services.session_store import sessions
from src.eir.questions import QUESTIONS
from fastapi import APIRouter, HTTPException

from ..schemas.session import SessionCreate, SessionResponse


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("", response_model=SessionResponse)
async def create_session(data: SessionCreate):
    session_id = str(uuid4())

    session = {
        "session_id": session_id,
        "patient_id": data.patient_id,
        "current_question": QUESTIONS[0]["question"],
        "answers": []
    }
    sessions[session_id] = session
    return SessionResponse(
        session_id= session_id,
        patient_id=data.patient_id,
        current_section=QUESTIONS[0]["section"],
        current_question=QUESTIONS[0]["question"],
    )

@router.post("/{session_id}/answers")
async def submit_answer(
    session_id: str,
    data: dict
):

    session = sessions.get(session_id)


    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    answer = data["answer"]

    session["answers"].append({
        "question": session["current_question"],
        "answer": answer
    })
    return {
        "message": "Answer recorded",
        "session_id": session_id
    }