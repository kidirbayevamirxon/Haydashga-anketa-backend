from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.admin import Admin
from app.schemas.auth import (
    AdminLoginRequest,
    ParticipantStartRequest,
    ParticipantStartResponse,
    TokenResponse,
)
from app.models.respondent import Respondent
from app.services.auth import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/api",
    tags=["Auth"],
)


@router.post(
    "/admin/login",
    response_model=TokenResponse,
)
def admin_login(
    data: AdminLoginRequest,
    db: Session = Depends(get_db),
):
    admin = db.scalar(
        select(Admin).where(
            Admin.username == data.username
        )
    )

    # Birinchi ishga tushishda default admin yaratish
    if admin is None:
        if (
            data.username == settings.ADMIN_USERNAME
            and data.password == settings.ADMIN_PASSWORD
        ):
            admin = Admin(
                username=settings.ADMIN_USERNAME,
                password_hash=hash_password(
                    settings.ADMIN_PASSWORD
                ),
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)
        else:
            raise HTTPException(
                status_code=401,
                detail="Login yoki parol noto'g'ri",
            )

    if not verify_password(
        data.password,
        admin.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Login yoki parol noto'g'ri",
        )

    token = create_access_token(
        {
            "sub": str(admin.id),
            "username": admin.username,
            "role": "admin",
        }
    )

    return TokenResponse(
        access_token=token,
    )


@router.post(
    "/auth/start",
    response_model=ParticipantStartResponse,
)
def start_participant(
    data: ParticipantStartRequest,
    db: Session = Depends(get_db),
):
    respondent = Respondent(
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
    )

    db.add(respondent)
    db.commit()
    db.refresh(respondent)

    return ParticipantStartResponse(
        id=str(respondent.id),
        first_name=respondent.first_name,
        last_name=respondent.last_name,
    )