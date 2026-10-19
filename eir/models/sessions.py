from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eir.db.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import Enum
from eir.models.enum import SessionStatus

if TYPE_CHECKING:
    from eir.models.patients import Patient

if TYPE_CHECKING:
    from eir.models.answers import Answer

class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        index=True,
    )
    patient_id: Mapped[str] = mapped_column(
        ForeignKey("patients.patient_id"),
        nullable=False,
        index=True,
    )
    current_question_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    status: Mapped[SessionStatus] = mapped_column(
        Enum(
            SessionStatus,
            name="session_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=SessionStatus.IN_PROGRESS,
        nullable=False,
    )
    patient: Mapped["Patient"] = relationship(
        back_populates="sessions",
    )
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Answer.created_at",
    )
