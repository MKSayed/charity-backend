from sqlmodel import Field, SQLModel
from datetime import datetime


class TimeStampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None,
        sa_column_kwargs={"onupdate": datetime.now}
    )
