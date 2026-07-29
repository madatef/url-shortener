import uuid

from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import decode_access_token
from app.core.error_registry import INVALID_TOKEN, USER_NOT_FOUND
from app.core.errors import AppError
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.repositories.user import user_repo


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_db),
) -> User:
    """
    Resolve the authenticated user from the access_token cookie.

    Raises:
        AppError(INVALID_TOKEN): cookie is missing, malformed, or expired
        AppError(USER_NOT_FOUND): token is valid but the user is gone
    """
    if access_token is None:
        raise AppError(INVALID_TOKEN)

    subject = decode_access_token(access_token)

    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise AppError(INVALID_TOKEN)

    user = await user_repo.get_by_id(session=session, user_id=user_id)
    if user is None:
        raise AppError(USER_NOT_FOUND)

    return user
