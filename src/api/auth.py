from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.users import create_user, get_user_by_email
from src.database.db import get_db
from src.schemas.auth import TokenModel
from src.schemas.user import UserCreate, UserLogin, UserResponse
from src.services.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    existing_user = await get_user_by_email(db, body.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
        )

    user = await create_user(db, body, get_password_hash(body.password))
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenModel)
async def login_user(
    body: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenModel:
    user = await authenticate_user(db, body.email, body.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return TokenModel(access_token=access_token)
