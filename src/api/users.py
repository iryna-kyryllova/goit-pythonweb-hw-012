from fastapi import APIRouter, Depends, File, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users import User
from src.services.auth import get_current_user, get_current_admin_user
from src.services.users import UserService
from src.services.upload_file import UploadFileService
from src.conf import messages
from src.conf.config import settings
from src.database.db import get_db

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=User, description=messages.REQUESTS_LIMIT)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    """
    Retrieve the currently authenticated user's details.

    Args:
        request: The incoming request object.
        user: The currently authenticated user.

    Returns:
        The User object representing the authenticated user.
    """
    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the avatar of an admin user.

    Args:
        file: The uploaded image file to be used as an avatar.
        admin: The currently authenticated admin user (ensures only admins can perform this action).
        db: Database session dependency.

    Returns:
        The updated User object with the new avatar URL.

    Raises:
        HTTPException: If the user is not an admin.
    """
    avatar_url = UploadFileService(
        settings.CLD_NAME, settings.CLD_API_KEY, settings.CLD_API_SECRET
    ).upload_file(file, admin.username)

    user_service = UserService(db)
    updated_admin = await user_service.update_avatar_url(admin.email, avatar_url)

    return updated_admin
