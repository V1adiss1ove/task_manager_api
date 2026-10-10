from fastapi import APIRouter

from app.schemas.token import LoginRequest, TokenResponse
from app.services.user import ServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    service: ServiceDep,
):
    return await service.authenticate(payload)
