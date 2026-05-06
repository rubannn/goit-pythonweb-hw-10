from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.models  # noqa: F401
from src.api.auth import router as auth_router
from src.api.contacts import router as contacts_router
from src.api.users import router as users_router
from src.database.config import settings
from src.database.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="REST API for storing and managing contacts.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["healthcheck"])
def read_root() -> dict[str, str]:
    return {"message": "Contacts API is running"}


app.include_router(contacts_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
