from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import hash_password


class UserRepo:
    async def create(
        *,
        session: AsyncSession, 
        username: str, 
        password: str
    ) -> User:
        user = User(
            username=username,
            hashed_password=hash_password(password),
        )

        session.add(user)
        try:
            await session.flush()
            await session.refresh(user)
        except IntegrityError as e:
            await session.rollback()
            raise Exception(str(e))
    
    async def get(session: AsyncSession, *, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        try:
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()
            return user
        except IntegrityError as e:
            raise Exception(str(e))


# Global Singleton
user_repo = UserRepo()