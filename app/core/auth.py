from datetime import timedelta, timezone, datetime

from jose import jwt, JWTError

from app.config import settings
from app.core.error_registry import INVALID_TOKEN
from app.core.errors import AppError


def _now() -> datetime:
    return datetime.now(timezone.utc)

def create_access_token(
    *,
    subject: str,
    expires_delta: timedelta = None, 
) -> tuple[str, str]:
    """
    Create a signed JWT access token.
    Returns:
        a tuple (access_token, expiry)
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)

    expire  = _now() + expires_delta
    payload = {
        "sub": subject,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return token, expire.isoformat() 

def decode_access_token(token: str) -> str:
    """
    Validate and decode JWT access token
    Returns:
        the subject of the token (user ID in our case)
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise AppError(INVALID_TOKEN)

    subject = payload.get("sub")
    if subject is None:
        raise AppError(INVALID_TOKEN)

    return subject