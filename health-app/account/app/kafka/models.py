import uuid
from typing import Any

from faust import Record


class TokenEvent(Record):
    token_id: str | uuid.UUID
    user_id: int


class AccountInfo(Record):
    user_id: int
    detail: dict[str, str | dict]


class Timetable(Record):
    doctor_id: int
    timetable: list[dict[str, Any]]
