import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class UserRepo:
    @staticmethod
    async def create(
        *,
        session: AsyncSession, 
        username: str, 
        hashed_password: str
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
        )

        session.add(user)
        try:
            await session.flush()
            await session.refresh(user)
            return user
        except IntegrityError as e:
            await session.rollback()
            raise e
    
    @staticmethod
    async def get(*, session: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()
        return user

    @staticmethod
    async def get_by_id(*, session: AsyncSession, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()
        return user


# Global Singleton
user_repo = UserRepo()