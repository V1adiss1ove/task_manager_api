from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import RepoDep, UserRepository
from app.schemas.user import SUserCreate


class UserService:
    """Бизнес-логика для работы с пользователем.

    Слой между HTTP-роутерами и репозиторием. Здесь выполняется:
    проверка уникальности email, хеширование пароля, выброс HTTP-ошибок.
    Данный слой SQL не пишет - все запросы к БД делегирует в UserRepository.
    """

    def __init__(self, repo: UserRepository):
        # Репозиторий приходит снаружи (DI), чтобы сервис не знал,
        # откуда берутся данные: Postgres, кэш или фейк в тестах.
        self.repo = repo

    async def register(self, data: SUserCreate) -> User:
        """Зарегистрировать нового пользователя.

        1. Проверяет, что email еще не занят (иначе 409 Conflict).
        2. Хеширует пароль - в БД уходит хеш, не открытый пароль.
        3. Делегирует создание в репозиторий.

        Именно здесь, а не в репозитории, живёт правило "email уникален":
        репозиторий просто отдаёт данные, решение принимает сервис.
        """

        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        hashed = hash_password(password=data.password)

        return await self.repo.create(data=data, hashed_password=hashed)

    async def get(self, user_id: int) -> User:
        """Получить пользователя по id или вернуть 404.

        Репозиторий возвращает User | None, а сервис превращает None
        в HTTP-ошибку.
        """

        user = await self.repo.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    async def list(self, skip: int = 0, limit: int = 20) -> list[User]:
        """Вернуть список пользователей с пагинацией.

        Обертка над репозиторием. Нужна для единообразия:
        роутер всегда работает с сервисом, а не с репозиторием напрямую -
        если позже добавится фильтрация или сортировк, место уже есть.
        """

        return await self.repo.list(skip=skip, limit=limit)


async def get_user_service(repo: RepoDep) -> UserService:
    return UserService(repo)


ServiceDep = Annotated[UserService, Depends(get_user_service)]
