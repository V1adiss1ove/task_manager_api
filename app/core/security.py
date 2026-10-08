from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

# -- Пароли --------------------------------------------------------------------------


def hash_password(password: str) -> str:
    """Хеширует пароль. Возвращает строку, готовую к записи в БД."""
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password=password.encode("utf-8"), salt=salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Проверяет, что пароль соответсвует хешу."""
    return bcrypt.checkpw(
        password=password.encode("utf-8"), hashed_password=hashed.encode("utf-8")
    )


# -- JWT -----------------------------------------------------------------------------


def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    """
    Создаёт JWT. subject — это user.id (в виде строки).
    expires_minutes — время жизни; по умолчанию из настроек.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    """Возвращает payload или None, если токен невалиден/истёк."""

    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
