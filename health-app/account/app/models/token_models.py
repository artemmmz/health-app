from datetime import datetime

from app.models.base import BaseModel
from app.utils.enums import TokenStatus


class Tokens(BaseModel):
    """Access and refresh tokens model."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class TokenPayload(BaseModel):
    """Full information about token."""

    sub: str
    user_id: int
    jti: str
    iat: datetime
    exp: datetime
    type: str
    status: TokenStatus
