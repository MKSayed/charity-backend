from sqlmodel import Field, SQLModel
from src.models.minxin import CreatedUpdatedAtMixin


class ServiceBase(SQLModel):
    name: str = Field(max_length=25, index=True)


class Service(ServiceBase, CreatedUpdatedAtMixin, table=True):
    id: int | None = Field(None, primary_key=True)
    active: bool = Field(default=True)
    description: str | None


class ServicePublic(ServiceBase):
    id: int
    active: bool


class ServiceCreate(ServiceBase):
    pass
