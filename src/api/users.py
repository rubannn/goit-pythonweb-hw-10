from fastapi import APIRouter, Depends, Request

from src.database.config import settings
from src.models.user import User
from src.schemas.user import UserResponse
from src.services.auth import get_current_user
from src.services.rate_limiter import limiter


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
@limiter.limit(settings.RATE_LIMIT_ME)
async def read_users_me(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    _ = request
    return UserResponse.model_validate(current_user)
