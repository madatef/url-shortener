import uuid

from sqlalchemy import ForeignKey, Index, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Url(BaseModel):
    __tablename__ = 'urls'

    key: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index(
            'uq_user_key',
            'key',
            'user_id',
            unique=True,
        ),
    )

    user = relationship('User', back_populates='urls')