from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime
from src.models.minxin import CreatedUpdatedAtMixin


class ServiceBase(SQLModel):
    name: str = Field(max_length=25, index=True)
    description: str | None


class Service(ServiceBase, CreatedUpdatedAtMixin, table=True):
    id: int | None = Field(None, primary_key=True)
    active: bool = Field(default=True)


class ServiceCreate(ServiceBase):
    pass

