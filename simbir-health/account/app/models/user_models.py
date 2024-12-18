from enum import Enum

from sqlmodel import Field
from sqlalchemy import Column, Integer

from pydantic import SecretStr

from app.models import BaseModel
from app.utils.enums import Role


class TableModel(BaseModel, table=True):
    id_: int | None = Field(
        default=None,
        sa_column=Column(
            Integer, name='id', autoincrement=True, primary_key=True
        )
    )


class BaseAccount(BaseModel):
    first_name: str
    last_name: str
    username: str


class User(BaseAccount, TableModel):
    roles: list[str] = Field(default=list(Role.USER.value))
    password: SecretStr


class AccountCreation(BaseAccount):
    password1: SecretStr
    password2: SecretStr


class AccountUpdate(BaseModel):
    first_name: str
    last_name: str
    password: SecretStr


class Authentication(BaseModel):
    username: str
    password: SecretStr


class GetAccounts(BaseModel):
    from_: int = Field(alias='from')
    count: int
