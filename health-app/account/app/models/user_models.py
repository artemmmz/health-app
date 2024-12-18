import re
from typing import Self

from pydantic import SecretStr, field_validator, model_validator
from sqlalchemy import Column, Integer
from sqlmodel import Field, Enum, Relationship, UniqueConstraint, String

from app.models import BaseModel
from app.utils.enums import Role


class BaseTableModel(BaseModel):
    __abstract__ = True

    id_: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={
            'autoincrement': True,
            'name': 'id'
        },
    )


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(
        min_length=3,
        max_length=50,
        regex=r'^[a-z0-9_-]*$'
    )


class UserRole(BaseTableModel, table=True):
    __tablename__ = 'user_role'
    __table_args__ = (UniqueConstraint('user_id', 'role'), )

    user_id: int | None = Field(
        default=None,
        foreign_key='users.id',
        primary_key=True,
        ondelete='CASCADE'
    )
    role: Role = Field(default=Role.USER, sa_column_args=(Enum(Role), ))

    user: 'User' = Relationship(back_populates='roles')


class User(BaseUser, BaseTableModel, table=True):
    __tablename__ = 'users'

    password: str

    roles: list[UserRole] = Relationship(
        back_populates='user',
        link_model=UserRole
    )


class UserAdd(BaseUser):
    password1: SecretStr
    password2: SecretStr

    @field_validator('password2')
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        password = v.get_secret_value()
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters')
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'\W', password):
            raise ValueError('Password must contain at least one special character')
        return v

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password1 != self.password2:
            raise ValueError('Passwords do not match')
        return self



class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    password: SecretStr


class Authentication(BaseModel):
    username: str
    password: SecretStr


class UserGet(BaseModel):
    from_: int = Field(title='from')
    count: int
