from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, field_validator


class UrlCreate(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def validate_value(cls, v: str) -> str:
        # AnyHttpUrl only, so schemes like javascript: and data: are
        # rejected — a stored javascript: URL would execute on redirect.
        # Validated then discarded: str keeps the value byte-for-byte,
        # whereas AnyHttpUrl normalises it (appends a trailing slash).
        AnyHttpUrl(v)
        return v


class UrlResponse(BaseModel):
    key: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True
