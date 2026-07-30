from pydantic import BaseModel, Field


class SurveyAnswerCreate(BaseModel):
    question_id: str
    question: str
    value: int = Field(ge=1, le=5)
    label: str


class GeneralInfo(BaseModel):
    gender: str
    age: str
    area: str
    experience: str
    occupation: str = Field(min_length=1, max_length=150)


class SurveyCreate(BaseModel):
    respondent_id: str

    general: GeneralInfo

    answers: list[SurveyAnswerCreate]

    opinion: str | None = None


class SurveyCreateResponse(BaseModel):
    survey_id: str
    respondent_id: str

    total_risk_score: int
    average_risk_level: float

    message: str


class AnswerResponse(BaseModel):
    question_id: str
    question: str
    value: int
    label: str


class SurveyDetailResponse(BaseModel):
    survey_id: str
    respondent_id: str

    first_name: str
    last_name: str

    gender: str
    age: str
    area: str
    experience: str
    occupation: str

    opinion: str | None

    total_risk_score: int
    average_risk_level: float

    answers: list[AnswerResponse]

    created_at: str