from fastapi.testclient import TestClient
from app import app
from eir.schemas.session import SessionResponse
from uuid import uuid4
from eir.services.questions import QUESTIONS
from eir.schemas.question import Question
from eir.schemas.answers import AnswerResponse, GiveAnswer
client = TestClient(app)

def test_create_session():
    patient_id = str(uuid4())
    response = client.post("/sessions", json= {"patient_id": patient_id})
    assert response.status_code == 201
    session = SessionResponse.model_validate(response.json())
    assert session.session_id
    assert session.patient_id == patient_id
    assert session.completed is False
    assert session.current_question is not None

def test_submit_answers_until_completion():

    question_bank = [
        Question.model_validate(question)
        for question in QUESTIONS
    ]

    assert question_bank, "Question bank must not be empty"

    create_response = client.post(
        "/sessions",
        json={"patient_id": str(uuid4())},
    )

    assert create_response.status_code == 201

    session = SessionResponse.model_validate(
        create_response.json()
    )

    session_id = session.session_id
    assert session_id

    for _ in range(len(question_bank)):
        current_question = session.current_question

        assert current_question in question_bank

        current_index = question_bank.index(current_question)
        is_last_question = current_index == len(question_bank) - 1

        answer_text = f"Test response {current_index + 1}"

        answer_request = GiveAnswer(answer=answer_text)

        response = client.post(
            f"/sessions/{session_id}/answers",
            json=answer_request.model_dump(),
        )

        assert response.status_code == 200

        result = AnswerResponse.model_validate(response.json())

        assert result.session_id == session_id
        assert result.answer == answer_text
        assert result.recorded is True
        assert result.completed is is_last_question

        if is_last_question:
            assert result.next_question is None
        else:
            expected_next_question = question_bank[current_index + 1]

            assert result.next_question == expected_next_question

            session.current_question = result.next_question

