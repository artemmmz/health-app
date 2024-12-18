from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    """Base abstract model."""

    __abstract__ = True


class BaseTableModel(BaseModel):
    """Base abstract database model with id column."""

    __abstract__ = True

    id_: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={'autoincrement': True, 'name': 'id'},
        alias='id',
        title='id',
    )


class BaseTableActiveModel(BaseTableModel):
    """Base abstract database model with id and is_active column."""

    __abstract__ = True

    is_active_: bool = Field(
        default=True, sa_column_kwargs={'name': 'is_active'}
    )

    @property
    def is_active(self) -> bool:
        return self.is_active_
