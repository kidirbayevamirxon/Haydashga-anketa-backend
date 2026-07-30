import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Survey(Base):
    __tablename__ = "surveys"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    respondent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("respondents.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    gender: Mapped[str] = mapped_column(String(30))
    age: Mapped[str] = mapped_column(String(30))
    area: Mapped[str] = mapped_column(String(100))
    experience: Mapped[str] = mapped_column(String(50))
    occupation: Mapped[str] = mapped_column(String(150))

    opinion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    total_risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    average_risk_level: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    respondent = relationship(
        "Respondent",
        back_populates="survey",
    )

    answers = relationship(
        "SurveyAnswer",
        back_populates="survey",
        cascade="all, delete-orphan",
    )


class SurveyAnswer(Base):
    __tablename__ = "survey_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    survey_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("surveys.id", ondelete="CASCADE"),
        nullable=False,
    )

    question_id: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    survey = relationship(
        "Survey",
        back_populates="answers",
    )