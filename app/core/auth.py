from datetime import timedelta, timezone, datetime

from jose import jwt, JWTError

from app.config import settings


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
            settings.ALGORITHM,
        )
    except JWTError as e:
        print(f'Failed to decode token: {str(e)}')
        raise Exception(str(e))

    subject = payload.get("subject")
    if subject is None:
        raise Exception("Invalid token")

    return subject