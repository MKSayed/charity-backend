from datetime import datetime
from enum import StrEnum
from typing import Any
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class EventType(StrEnum):
    processing = "P"
    success = "S"
    failed = "F"


class TransactionLogBase(SQLModel):
    event_details: str | None
    event_type: EventType
    transaction_uuid: UUID = Field(foreign_key="transaction.uuid")


class TransactionLog(TransactionLogBase, table=True):
    __tablename__: Any = "transaction_log"

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
