from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import SUserCreate, SUserResponse
from app.services.user import ServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=SUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(payload: SUserCreate, service: ServiceDep):
    return await service.register(payload)


@router.get("/me", response_model=SUserResponse)
async def get_me(current: User = Depends(get_current_user)):
    return current


@router.get("/{user_id}", response_model=SUserResponse)
async def get_user(user_id: int, service: ServiceDep):
    return await service.get(user_id)


@router.get("/", response_model=list[SUserResponse])
async def list_users(service: ServiceDep, skip: int = 0, limit: int = 20):
    return await service.list(skip=skip, limit=limit)
