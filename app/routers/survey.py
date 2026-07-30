from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.respondent import Respondent
from app.models.survey import Survey
from app.schemas.survey import (
    SurveyCreate,
    SurveyCreateResponse,
    SurveyDetailResponse,
    AnswerResponse,
)
from app.services.survey import create_survey


router = APIRouter(
    prefix="/api/surveys",
    tags=["Surveys"],
)


@router.post(
    "",
    response_model=SurveyCreateResponse,
)
def submit_survey(
    data: SurveyCreate,
    db: Session = Depends(get_db),
):
    survey = create_survey(
        db=db,
        data=data,
    )

    return SurveyCreateResponse(
        survey_id=str(survey.id),
        respondent_id=str(survey.respondent_id),
        total_risk_score=survey.total_risk_score,
        average_risk_level=survey.average_risk_level,
        message="Anketa muvaffaqiyatli saqlandi",
    )


@router.get(
    "/{survey_id}",
    response_model=SurveyDetailResponse,
)
def get_survey(
    survey_id: str,
    db: Session = Depends(get_db),
):
    survey = db.scalar(
        select(Survey).where(
            Survey.id == survey_id
        )
    )

    if survey is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Anketa topilmadi",
        )

    respondent = survey.respondent

    return SurveyDetailResponse(
        survey_id=str(survey.id),
        respondent_id=str(respondent.id),

        first_name=respondent.first_name,
        last_name=respondent.last_name,

        gender=survey.gender,
        age=survey.age,
        area=survey.area,
        experience=survey.experience,
        occupation=survey.occupation,

        opinion=survey.opinion,

        total_risk_score=survey.total_risk_score,
        average_risk_level=survey.average_risk_level,

        answers=[
            AnswerResponse(
                question_id=answer.question_id,
                question=answer.question,
                value=answer.value,
                label=answer.label,
            )
            for answer in survey.answers
        ],

        created_at=survey.created_at.isoformat(),
    )