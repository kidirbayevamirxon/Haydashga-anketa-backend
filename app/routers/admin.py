from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.respondent import Respondent
from app.models.survey import Survey
from app.services.dependencies import get_current_admin


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
)


@router.get("/respondents")
def get_respondents(
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    respondents = db.scalars(
        select(Respondent)
        .order_by(
            Respondent.created_at.desc()
        )
    ).all()

    result = []

    for respondent in respondents:
        survey = respondent.survey

        result.append(
            {
                "id": str(respondent.id),
                "first_name": respondent.first_name,
                "last_name": respondent.last_name,
                "created_at": respondent.created_at.isoformat(),

                "gender": (
                    survey.gender
                    if survey
                    else None
                ),

                "age": (
                    survey.age
                    if survey
                    else None
                ),

                "area": (
                    survey.area
                    if survey
                    else None
                ),

                "occupation": (
                    survey.occupation
                    if survey
                    else None
                ),

                "total_risk_score": (
                    survey.total_risk_score
                    if survey
                    else None
                ),

                "average_risk_level": (
                    survey.average_risk_level
                    if survey
                    else None
                ),
            }
        )

    return result


@router.get("/respondents/{respondent_id}")
def get_respondent(
    respondent_id: str,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    respondent = db.scalar(
        select(Respondent).where(
            Respondent.id == respondent_id
        )
    )

    if respondent is None:
        raise HTTPException(
            status_code=404,
            detail="Respondent topilmadi",
        )

    survey = respondent.survey

    if survey is None:
        return {
            "id": str(respondent.id),
            "first_name": respondent.first_name,
            "last_name": respondent.last_name,
            "survey": None,
        }

    return {
        "id": str(respondent.id),
        "first_name": respondent.first_name,
        "last_name": respondent.last_name,

        "survey": {
            "id": str(survey.id),
            "gender": survey.gender,
            "age": survey.age,
            "area": survey.area,
            "experience": survey.experience,
            "occupation": survey.occupation,
            "opinion": survey.opinion,

            "total_risk_score": survey.total_risk_score,
            "average_risk_level": survey.average_risk_level,

            "created_at": survey.created_at.isoformat(),

            "answers": [
                {
                    "question_id": answer.question_id,
                    "question": answer.question,
                    "value": answer.value,
                    "label": answer.label,
                }
                for answer in survey.answers
            ],
        },
    }


@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    total_respondents = db.scalar(
        select(func.count(Respondent.id))
    ) or 0

    total_surveys = db.scalar(
        select(func.count(Survey.id))
    ) or 0

    average_risk = db.scalar(
        select(func.avg(Survey.average_risk_level))
    )

    return {
        "total_respondents": total_respondents,
        "total_surveys": total_surveys,
        "average_risk_level": round(
            float(average_risk or 0),
            2,
        ),
    }