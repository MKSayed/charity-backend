from sqlmodel import SQLModel, Field, Column, DateTime
from datetime import datetime


class CreatedUpdatedAtMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        sa_column=Column(DateTime, onupdate=datetime.now)
    )
