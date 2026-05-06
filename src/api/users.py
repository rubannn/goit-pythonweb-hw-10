from fastapi import APIRouter, Depends

from src.models.user import User
from src.schemas.user import UserResponse
from src.services.auth import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)
