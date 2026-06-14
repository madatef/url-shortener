from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ErrorContract:
    code: str
    status_code: int
    message: str
    field: Optional[str] = None


# ------------------
# Auth domain errors
# ------------------

INVALID_CREDENTIALS = ErrorContract(
    code="invalid_credentials",
    message="Invalid username or password.",
    status_code=401,
)

USER_EXISTS = ErrorContract(
    code="email_exists",
    message="A user with this username already exists.",
    status_code=409,
)

INVALID_TOKEN = ErrorContract(
    code="invalid_token",
    message="Token is invalid or has expired.",
    status_code=401,
)

USER_NOT_FOUND = ErrorContract(
    code="user_not_found",
    message="User doesn't exist.",
    status_code=404,
)