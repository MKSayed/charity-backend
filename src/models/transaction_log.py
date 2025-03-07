from datetime import datetime
from enum import StrEnum
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class EventType(StrEnum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class TransactionLogBase(SQLModel):
    event_details: str | None
    event_type: EventType
    # transaction: Transaction


class TransactionLog(TransactionLogBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
