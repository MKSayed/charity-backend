from sqlmodel import Field, SQLModel
from src.models.mixin import TimeStampMixin


class ServiceBase(SQLModel):
    name: str = Field(max_length=25, index=True)
    description: str | None = None


class Service(ServiceBase, TimeStampMixin, table=True):
    id: int | None = Field(None, primary_key=True)
    active: bool = Field(default=True)


class ServicePublic(ServiceBase):
    id: int
    active: bool


class ServiceCreate(ServiceBase):
    pass
