import uuid
from typing import Any, Optional

from faust import Record

from app.utils.enums import SessionAction


class Session(Record, serializer='json'):
    access_token: str
    action: SessionAction = SessionAction.CREATE
    token_type: str = 'Bearer'
    expires_in: Optional[int] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
