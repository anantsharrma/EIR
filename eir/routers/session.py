from uuid import uuid4
from eir.services.session_store import sessions
from eir.services.questions import QUESTIONS
from fastapi import APIRouter, HTTPException
from eir.schemas.session import SessionCreate, SessionResponse, SessionState
from eir.schemas.answers import AnswerResponse, RecordedAnswer, GiveAnswer
router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("", response_model=SessionResponse)
async def create_session(data: SessionCreate) -> SessionResponse:
    session_id = str(uuid4())

    sessions[session_id] = SessionState(session_id=session_id,
                                        patient_id=data.patient_id,)
    session = sessions[session_id]
    return SessionResponse(
        session_id= session.session_id,
        patient_id=session.patient_id,
        current_question=QUESTIONS[session.question_index],
        completed= session.completed,
    )

@router.post("/{session_id}/answers", response_model=AnswerResponse)
async def submit_answer(
    session_id: str,
    data: GiveAnswer
) -> AnswerResponse:
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    if session.completed:
        raise HTTPException(
            status_code=409,
            detail="Session already completed"
        )
    index = session.question_index
    current_question = QUESTIONS[index]

    recorded_answer = RecordedAnswer(
        question_id=current_question.question_id,
        question_text=current_question.prompt,
        answer=data.answer,
    )
    session.answers.append(recorded_answer)
    index += 1
    next_question= QUESTIONS[index]
    if index >= len(QUESTIONS):
        session.completed=True
        return AnswerResponse(
            session_id=session.session_id,
            answer=session.answers[0].answer,
            next_question=None,
            recorded=True,
            completed=True,
        )
    return AnswerResponse(
        session_id=session.session_id,
        answer=session.answers[0].answer,
        recorded=True,
        next_question=next_question,
        completed=False,
    )
