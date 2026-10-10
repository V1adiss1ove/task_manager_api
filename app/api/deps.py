from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.models.user import User
from app.repositories.user import RepoDep

# tokenUrl — только для Swagger UI, чтобы появилась кнопка "Authorize"
bearer_scheme = HTTPBearer()


async def get_current_user(
    repo: RepoDep,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:

    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise credentials_exc

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exc

    user = await repo.get(int(user_id))
    if not user:
        raise credentials_exc

    return user
