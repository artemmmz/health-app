from sqlmodel import UniqueConstraint, Field, Relationship, Enum

from app.models.base import BaseTableActiveModel
from app.utils.enums import Role


class UserRole(BaseTableActiveModel, table=True):
    """User role database model."""

    __tablename__ = 'user_role'
    __table_args__ = (
        UniqueConstraint('user_id', 'role', name='user_id_role'),
    )

    user_id: int | None = Field(
        default=None,
        foreign_key='users.id',
        primary_key=True,
        ondelete='CASCADE',
    )
    role: Role = Field(default=Role.USER, sa_column_args=(Enum(Role),))

    user: 'User' = Relationship(  # type: ignore  # noqa: F821
        back_populates='roles'
    )
