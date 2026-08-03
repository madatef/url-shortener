import uuid
from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_registry import KEY_GENERATION_FAILED, URL_NOT_FOUND
from app.core.errors import AppError
from app.core.keygen import generate_key
from app.models.url import Url
from app.repositories.url import url_repo


MAX_KEY_ATTEMPTS = 5


async def create_url(
    *,
    session: AsyncSession,
    value: str,
    user_id: uuid.UUID,
) -> Url:
    """
    Allocate a short code for value and persist it.

    Raises:
        AppError(KEY_GENERATION_FAILED): no free code found in
            MAX_KEY_ATTEMPTS tries
    """
    for _ in range(MAX_KEY_ATTEMPTS):
        key = generate_key()

        existing = await url_repo.get_by_key(session=session, key=key)
        if existing is not None:
            continue

        try:
            url = await url_repo.create(
                session=session,
                key=key,
                value=value,
                user_id=user_id,
            )
        # safety net for race conditions: another request may have taken
        # this key between the check above and the insert
        except IntegrityError:
            continue
        except Exception:
            await session.rollback()
            raise

        await session.commit()
        return url

    raise AppError(KEY_GENERATION_FAILED)


async def get_url_by_key(*, session: AsyncSession, key: str) -> Url:
    """
    Resolve a short code for redirection.

    Not owner-scoped by design — anyone holding the link can follow it.

    Raises:
        AppError(URL_NOT_FOUND): no such short code
    """
    url = await url_repo.get_by_key(session=session, key=key)
    if url is None:
        raise AppError(URL_NOT_FOUND)

    return url


async def list_urls(
    *,
    session: AsyncSession,
    user_id: uuid.UUID,
) -> Sequence[Url]:
    return await url_repo.list_for_user(session=session, user_id=user_id)


async def delete_url(
    *,
    session: AsyncSession,
    key: str,
    user_id: uuid.UUID,
) -> None:
    """
    Delete a short code belonging to user_id.

    Raises:
        AppError(URL_NOT_FOUND): no such code, or it belongs to someone
            else — the two are reported identically so the endpoint does
            not confirm the existence of other users' codes
    """
    try:
        deleted = await url_repo.delete_for_user(
            session=session,
            key=key,
            user_id=user_id,
        )
    except Exception:
        await session.rollback()
        raise

    if not deleted:
        raise AppError(URL_NOT_FOUND)

    await session.commit()
