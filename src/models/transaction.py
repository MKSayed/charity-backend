from datetime import datetime
from enum import StrEnum
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from src.models.minxin import CreatedUpdatedAtMixin


class TransactionStatus(StrEnum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class POSInteractionMethod(StrEnum):
    contactless = "contactless"
    dipped = "dip"


class TransactionBase(SQLModel):
    service_id: int = Field(foreign_key="service.id")
    transaction_amount: float
    phone_no: str = Field(
        max_length=11, min_length=11, index=True
    )  # Egyptian phone numbers are always 11 digits
    status: TransactionStatus
    pos_interaction_method: POSInteractionMethod
    card_number: str
    terminal_id: str = Field(index=True)
    merchant_id: str = Field(index=True)
    ecr_ref_no: str
    trx_datetime: datetime


class Transaction(TransactionBase, CreatedUpdatedAtMixin, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
