from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_registry import INVALID_CREDENTIALS, USER_EXISTS
from app.core.errors import AppError
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token
from app.models.user import User
from app.repositories.user import user_repo


async def create_user(
    session: AsyncSession,
    *,
    username: str,
    password: str,
) -> tuple[User, dict[str, str]]:

    user = await user_repo.get(session=session, username=username)
    if user is not None:
        raise AppError(USER_EXISTS)

    hashed_password = hash_password(password)
    try:
        user = await user_repo.create(
            session=session,
            username=username,
            hashed_password=hashed_password,
        )

        token, expiry = create_access_token(subject=str(user.id))
        token = {
            'access_token': token,
            'expiry': expiry,
        }

        return user, token
    # safety net for race conditions
    except IntegrityError:
        raise AppError(USER_EXISTS)
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.commit()


async def login(
    *,
    session: AsyncSession,
    username: str,
    password: str,
) -> tuple[User, dict[str, str]]:

    user = await user_repo.get(session=session, username=username)
    if user is None or not verify_password(password, user.hashed_password):
        raise AppError(INVALID_CREDENTIALS)

    token, expiry = create_access_token(subject=str(user.id))
    token = {
        'access_token': token,
        'expiry': expiry,
    }
    
    return user, token