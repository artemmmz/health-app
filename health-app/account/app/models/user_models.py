import re
from typing import Self, List

from pydantic import SecretStr, field_validator, model_validator
from sqlmodel import Field, Relationship

from app.models.base import BaseModel, BaseTableActiveModel, BaseTableModel
from app.models.role_models import UserRole
from app.utils.enums import Role


class BaseUser(BaseModel):
    """Abstract user model."""

    __abstract__ = True

    first_name: str
    last_name: str
    username: str = Field(
        min_length=3, max_length=50, regex=r'^[a-z0-9_-]*$', unique=True
    )

    @field_validator('username')  # noqa
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-z0-9_-]*$', v):
            raise ValueError(
                'Username must contain only lowercase letters, '
                'numbers and underscore'
            )
        if not 3 <= len(v) <= 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return v


class UserModel(BaseUser, BaseTableModel):
    """User model."""

    ...  # fmt: off


class UserModelWithRoles(UserModel):
    """User model with roles."""

    roles: List[Role]


class User(BaseUser, BaseTableActiveModel, table=True):
    """User database model."""

    __tablename__ = 'users'

    password: str

    roles: list[UserRole] = Relationship(
        back_populates='user',
    )


class UserAdd(BaseUser):
    """User registration model."""

    password1: SecretStr
    password2: SecretStr

    @field_validator('password2')  # noqa
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        password = v.get_secret_value()
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters')
        if not re.search(r'[A-Z]', password):
            raise ValueError(
                'Password must contain at least one uppercase letter'
            )
        if not re.search(r'[a-z]', password):
            raise ValueError(
                'Password must contain at least one lowercase letter'
            )
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'\W', password):
            raise ValueError(
                'Password must contain at least one special character'
            )
        return v

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password1 != self.password2:
            raise ValueError('Passwords do not match')
        return self


class UserCreation(BaseUser):
    """User creation model."""

    password: SecretStr

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }


class UserCreationWithRoles(UserCreation):
    """User creation model with roles."""

    roles: list[Role]


class UserUpdate(BaseModel):
    """User update model."""

    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    password: SecretStr | None = Field(default=None)

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }


class UserUpdateFull(UserUpdate):
    """User update model for administrators."""

    username: str | None = Field(default=None)
    roles: list[Role] | None = Field(default=None)


class Authentication(BaseModel):
    """User authentication model."""

    username: str
    password: SecretStr

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }


class UserGet(BaseModel):
    """User get data model."""

    from_: int = Field(title='from', ge=0, default=0)
    count: int = Field(ge=1, le=100, default=100)


class DoctorGet(UserGet):
    """Doctor get data model."""

    name_filter: str = Field(default='')
