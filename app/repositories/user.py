"""Слой работы с БД.
Репозиторий — это прослойка между бизнес-логикой (сервисами) и базой данных.
Он инкапсулирует все SQL-запросы к одной таблице (или сущности) и
редоставляет сервисам понятный Python-интерфейс вместо сырых select()."""

from typing import Annotated

from db.session import SessionDep
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import SUserCreate


class UserRepository:
    """Репозитория для работы с таблицей users.

    Инкапсулирует все SQL-запросы к модели User.
    Сессия передается снаружи (DI), чтобы все репозитории
    в рамках одного запроса работали в одной транзакции.
    """

    def __init__(self, session: AsyncSession):
        # Сохраняем сессию как атрибут - будем использовать ее во всех методах.
        # Сессия приходит извне (FastAPI Depends), не создается здесь.
        self.session = session

    async def get(self, user_id: int) -> User | None:
        """Получить пользователя по первичному ключу (id).

        Использует session.get() - умеет отдавать объект из identity map
        (без SQL-запроса), если он уже загружен в текущей сессии.
        Возвращает None, если пользователь не найден.
        """

        # get - получить одну запись по первичному ключу
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Найти пользователя по email.

        Нужен для логина и проверки уникальности при регистрации.
        Возращает None, если совпадений нет.
        """

        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 20) -> list[User]:
        """Получить список пользователей с пагинацией.

        skip - сколько записей пропустить (offset).
        limit - максимум записей в ответе.
        Возвращает список ORM-объектов User (может быть пустым).
        """

        result = await self.session.execute(select(User).offset(skip).limit(limit))

        return list(result.scalars().all())

    async def create(self, data: SUserCreate, hashed_password: str) -> User:
        """Создать нового пользователя

        Принимает валидированные данные из Pydantic-схемы и
        захешированный пароль. Добавляет объект в сессию,
        коммитит и обновляет его из БД, чтобы вернуть
        актуальные поля (id, created_at и т.д.).
        """

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


RepoDep = Annotated[UserRepository, Depends(get_user_repository)]
