from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from eir.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from eir.models.sessions import Session
class Patient(Base):
    __tablename__ = 'patients'
    patient_id: Mapped[str] = mapped_column(
        primary_key=True,
        index=True,
    )
    patient_name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
    )
