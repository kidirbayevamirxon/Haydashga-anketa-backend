from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.respondent import Respondent
from app.models.survey import Survey, SurveyAnswer
from app.schemas.survey import SurveyCreate


EXPECTED_ANSWERS = 20


def create_survey(
    db: Session,
    data: SurveyCreate,
):
    respondent = db.scalar(
        select(Respondent).where(
            Respondent.id == data.respondent_id
        )
    )

    if respondent is None:
        raise HTTPException(
            status_code=404,
            detail="Respondent topilmadi",
        )

    existing = db.scalar(
        select(Survey).where(
            Survey.respondent_id == respondent.id
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Bu respondent anketani allaqachon to'ldirgan",
        )

    if len(data.answers) != EXPECTED_ANSWERS:
        raise HTTPException(
            status_code=422,
            detail=f"{EXPECTED_ANSWERS} ta savolga javob berish kerak",
        )

    # Backendning o'zi hisoblaydi
    total = sum(answer.value for answer in data.answers)

    average = round(
        total / len(data.answers),
        2,
    )

    survey = Survey(
        respondent_id=respondent.id,

        gender=data.general.gender,
        age=data.general.age,
        area=data.general.area,
        experience=data.general.experience,
        occupation=data.general.occupation,

        opinion=data.opinion,

        total_risk_score=total,
        average_risk_level=average,
    )

    db.add(survey)
    db.flush()

    for answer in data.answers:
        survey_answer = SurveyAnswer(
            survey_id=survey.id,
            question_id=answer.question_id,
            question=answer.question,
            value=answer.value,
            label=answer.label,
        )

        db.add(survey_answer)

    db.commit()
    db.refresh(survey)

    return survey