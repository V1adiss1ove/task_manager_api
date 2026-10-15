from fastapi import APIRouter, status

from app.api.deps import CurrUserDep
from app.schemas.user import SUserCreate, SUserResponse
from app.services.user import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=SUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(payload: SUserCreate, service: UserServiceDep):
    return await service.register(payload)


@router.get("/me", response_model=SUserResponse)
async def get_me(current: CurrUserDep):
    return current


@router.get("/{user_id}", response_model=SUserResponse)
async def get_user(user_id: int, service: UserServiceDep):
    return await service.get(user_id)


@router.get("/", response_model=list[SUserResponse])
async def list_users(service: UserServiceDep, skip: int = 0, limit: int = 20):
    return await service.list(skip=skip, limit=limit)
