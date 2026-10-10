from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Схема запроса на вход (login)"""

    email: EmailStr  # логин-идентификатор пользователя
    password: str


class TokenResponse(BaseModel):
    """Схема ответа с токеном доступа"""

    access_token: str  # jwt-token
    token_type: str = "bearer"  # тип схемы авторизации
