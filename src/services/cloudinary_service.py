import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, status
from fastapi import UploadFile

from src.database.config import settings


def _ensure_cloudinary_configured() -> None:
    if not all(
        [
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloudinary is not configured",
        )


def _configure_cloudinary() -> None:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


async def upload_avatar(file: UploadFile, user_id: int) -> str:
    _ensure_cloudinary_configured()
    _configure_cloudinary()

    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file",
        )

    result = cloudinary.uploader.upload(
        contents,
        folder="contacts_api/avatars",
        public_id=f"user_{user_id}",
        overwrite=True,
        resource_type="image",
    )
    return str(result["secure_url"])
