from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    body: UserCreate,
    hashed_password: str,
) -> User:
    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
