
from uuid import uuid4

from eir.schemas.answers import (
    GiveAnswer,
    AnswerResponse,
    RecordedAnswer,
)
from eir.schemas.session import SessionCreate, SessionResponse, SessionState
from eir.services.questions import QUESTIONS
from eir.services.session_store import sessions


class SessionNotFoundError(Exception):
    pass
class SessionAlreadyCompletedError(Exception):
    pass
class NoQuestionsConfiguredError(Exception):
    pass


def create_session(data: SessionCreate) -> SessionResponse:

    if not QUESTIONS:
        raise NoQuestionsConfiguredError("No questions are configured.")

    session_id = str(uuid4())
    session = SessionState(
        session_id=session_id,
        patient_id=data.patient_id,
    )
    sessions[session_id] = session

    return SessionResponse(
        session_id=session.session_id,
        patient_id=session.patient_id,
        current_question=QUESTIONS[session.question_index],
        completed=session.completed,
    )


def submit_answer(
    session_id: str,
    data: GiveAnswer,
) -> AnswerResponse:


    session = sessions.get(session_id)

    if session is None:
        raise SessionNotFoundError("Session not found.")

    if session.completed:
        raise SessionAlreadyCompletedError(
            "This session is already complete."
        )

    current_question = QUESTIONS[session.question_index]

    recorded_answer = RecordedAnswer(
        question_id=current_question.question_id,
        question_text=current_question.prompt,
        answer=data.answer,
    )

    session.answers.append(recorded_answer)
    session.question_index += 1

    if session.question_index >= len(QUESTIONS):
        session.completed = True

        return AnswerResponse(
            session_id=session.session_id,
            answer=recorded_answer.answer,
            recorded=True,
            next_question=None,
            completed=True,
        )

    next_question = QUESTIONS[session.question_index]

    return AnswerResponse(
        session_id=session.session_id,
        answer=recorded_answer.answer,
        recorded=True,
        next_question=next_question,
        completed=False,
    )
