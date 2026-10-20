
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from eir.models.sessions import Session as SessionModel
from eir.models.patients import Patient as PatientModel
from eir.models.answers import Answer as AnswerModel
from eir.schemas.answers import (
    GiveAnswer,
    AnswerResponse,
    RecordedAnswer,
)
from eir.schemas.session import SessionCreate, SessionResponse
from eir.services.questions import QUESTIONS
from eir.models.enum import SessionStatus
from eir.services.error.session import (
SessionNotFoundError,
SessionAlreadyCompletedError,
NoQuestionsConfiguredError,
PatientHasNoSessionsErorr
)
from eir.services.error.patient import PatientNotFoundError

async def create_session(
        data: SessionCreate,
        db: AsyncSession) -> SessionResponse:
    patient_result = await db.execute(select(PatientModel).where(PatientModel.patient_id == data.patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise PatientNotFoundError("Patient not found.")
    if not QUESTIONS:
        raise NoQuestionsConfiguredError("No questions are configured.")

    session = SessionModel(
        session_id=str(uuid4()),
        patient_id=data.patient_id,
        current_question_id=QUESTIONS[0].question_id,
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return SessionResponse(
        session_id=session.session_id,
        patient_id=session.patient_id,
        current_question=QUESTIONS[0],
        completed=session.completed,
    )

async def submit_answer(
    session_id: str,
    data: GiveAnswer,
    db: AsyncSession
) -> AnswerResponse:


    session_result = await db.execute(select(SessionModel).options(selectinload(SessionModel.answers)).where(SessionModel.session_id == session_id))
    session = session_result.scalar_one_or_none()
    if session is None:
        raise SessionNotFoundError("Session not found.")

    if session.status != SessionStatus.IN_PROGRESS:
        raise SessionAlreadyCompletedError(
            "This session is not accepting answers."
        )

    answer_q_id = {
        answer.question_id for answer in session.answers
    }
    current_question = next(
    (
        q for q in QUESTIONS
        if q.question_id not in answer_q_id
    ),
    None,
    )
    if current_question is None:
        raise NoQuestionsConfiguredError("No questions are configured.")
    recorded_answer = AnswerModel(
    session_id=session.session_id,
    question_id=current_question.question_id,
    question_text=current_question.prompt,
    answer_text=data.answer,
)
    db.add(recorded_answer)
    answer_q_id.add(current_question.question_id)
    next_question = next(
        (
            q for q in QUESTIONS
            if q.question_id not in answer_q_id
        ),
        None,
    )
    if next_question is None:
        session.current_question_id = None
        session.completed = True
        session.status = SessionStatus.COMPLETED
    else:
        session.current_question_id = next_question.question_id
    await db.commit()
    return AnswerResponse(
        session_id=session.session_id,
        answer=data.answer,
        recorded=True,
        next_question=next_question,
        completed=session.completed,
    )

async def get_all_session(
        patient_id: str,
        db: AsyncSession,
):
    result = await db.execute(
        select(PatientModel.patient_id, SessionModel.session_id)
        .outerjoin(
            SessionModel,
            PatientModel.patient_id == SessionModel.patient_id,
        )
        .where(PatientModel.patient_id == patient_id)
    )

    rows = result.all()

    if not rows:
        raise PatientNotFoundError("Patient not found.")

    session_ids = [
        row.session_id
        for row in rows
        if row.session_id is not None
    ]

    if not session_ids:
        raise PatientHasNoSessionsErorr("This patient has no sessions.")


    return {"session_ids": session_ids}

async def get_session(
        session_id:str,
        patient_id:str,
        db: AsyncSession
):
    result = await db.execute(
        select(SessionModel).options(selectinload(SessionModel.answers), selectinload(SessionModel.patient)).where(
            SessionModel.patient_id == patient_id, SessionModel.session_id == session_id))
    session = result.scalar_one_or_none()
    if session is None:
        raise SessionNotFoundError("Session not found.")
    return session

