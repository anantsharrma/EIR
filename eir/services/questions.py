from eir.schemas.question import Question, QuestionSection

QUESTIONS: list[Question] = [
    Question(
        question_id="Q001",
        section=QuestionSection.CHIEF_COMPLAINT,
        prompt="What is the main problem or symptom that brought you here?",
    ),
    Question(
        question_id="Q002",
        section=QuestionSection.DURATION,
        prompt="How long have you been experiencing this?",
    ),
    Question(
        question_id="Q003",
        section=QuestionSection.ASSOCIATED_SYMPTOMS,
        prompt="Are you experiencing any other symptoms?",
    ),
]