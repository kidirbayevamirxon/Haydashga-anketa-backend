from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.config import settings


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Password 72 bytes dan uzun bo'lishi mumkin emas"
        )

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")

    if len(password_bytes) > 72:
        return False

    return bcrypt.checkpw(
        password_bytes,
        hash_bytes,
    )


def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )
