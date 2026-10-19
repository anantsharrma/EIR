from datetime import datetime
from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eir.db.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from eir.models.sessions import Session

class Answer(Base):
    __tablename__ = "answers"

    session_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("sessions.session_id"),
        nullable=False,
        index=True,
        primary_key=True,
    )

    question_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        primary_key=True
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    answer_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped["Session"] = relationship(
        back_populates="answers",
    )