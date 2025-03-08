from datetime import datetime
from enum import StrEnum
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from src.models.mixin import TimeStampMixin


class TransactionStatus(StrEnum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class POSInteractionMethod(StrEnum):
    contactless = "contactless"
    dipped = "dip"


class TransactionBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)  # pyright: ignore

    transaction_amount: float
    phone_no: str = Field(
        max_length=11, min_length=11, index=True
    )  # Egyptian phone numbers are always 11 digits


class Transaction(TransactionBase, TimeStampMixin, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    service_id: int = Field(foreign_key="service.id")
    pos_interaction_method: POSInteractionMethod | None = None
    status: TransactionStatus
    card_number: str | None = None
    terminal_id: str | None = Field(default=None, index=True)
    merchant_id: str | None = Field(default=None, index=True)
    ecr_ref_no: str | None = None
    trx_datetime: datetime | None = None


class TransactionPublic(TransactionBase):
    service_id: int
    pos_interaction_method: POSInteractionMethod | None = None
    status: TransactionStatus
    ecr_ref_no: str | None = None
    trx_datetime: datetime | None = None


class TransactionCreate(TransactionBase):
    service_id: int
