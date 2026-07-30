from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

# Models import qilinishi shart
from app.models import (
    Admin,
    Respondent,
    Survey,
    SurveyAnswer,
)

from app.routers.auth import router as auth_router
from app.routers.survey import router as survey_router
from app.routers.admin import router as admin_router


Base.metadata.create_all(
    bind=engine
)

app = FastAPI(title="Axis Backend API", lifespan=lifespan, openapi_url="/openapi.json", root_path=os.getenv("ROOT_PATH", ""))



origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(survey_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Haydash Anketa API ishlayapti"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }