import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

class Url(BaseModel):
    __tablename__ = 'urls'

    # Globally unique: the redirect route resolves a short code with no
    # user context, so a key must map to exactly one destination.
    key: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # Not unique: two users may shorten the same destination, and one user
    # may want several codes for it. Indexed for lookups.
    value: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
    )

    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    user = relationship('User', back_populates='urls')
