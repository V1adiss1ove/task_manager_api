import bcrypt


def hash_password(password: str) -> str:
    """Хеширует пароль. Возвращает строку, готовую к записи в БД."""
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password=password.encode("utf-8"), salt=salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Проверяет, что пароль соответсвует хешу."""
    return bcrypt.checkpw(
        password=password.encode("utf-8"), hashed_password=hashed.encode("utf-8")
    )
