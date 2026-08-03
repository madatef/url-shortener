import uuid
from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.url import Url


class UrlRepo:
    @staticmethod
    async def create(
        *,
        session: AsyncSession,
        key: str,
        value: str,
        user_id: uuid.UUID,
    ) -> Url:
        url = Url(
            key=key,
            value=value,
            user_id=user_id,
        )

        # SAVEPOINT, so a key collision unwinds only this insert. A plain
        # rollback would discard the whole session and leave the caller
        # unable to retry with a freshly generated key.
        async with session.begin_nested():
            session.add(url)
            await session.flush()

        await session.refresh(url)
        return url

    @staticmethod
    async def get_by_key(*, session: AsyncSession, key: str) -> Url | None:
        stmt = select(Url).where(Url.key == key)
        res = await session.execute(stmt)
        url = res.scalar_one_or_none()
        return url

    @staticmethod
    async def list_for_user(
        *,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> Sequence[Url]:
        stmt = (
            select(Url)
            .where(Url.user_id == user_id)
            .order_by(Url.created_at.desc())
        )
        res = await session.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def delete_for_user(
        *,
        session: AsyncSession,
        key: str,
        user_id: uuid.UUID,
    ) -> bool:
        """
        Delete a short code owned by user_id.

        Returns:
            True if a row was deleted, False if no such key belongs to
            this user — the caller cannot distinguish "not found" from
            "someone else's", which is deliberate.
        """
        stmt = delete(Url).where(Url.key == key, Url.user_id == user_id)
        res = await session.execute(stmt)
        return res.rowcount > 0


# Global Singleton
url_repo = UrlRepo()
