from sqlmodel import Session
from src.models.transaction_log import EventType, TransactionLog
from src.utils.geidea_api import CheckStatusResult, TransactionResult


def create_processing_transaction_log(session: Session, trx_uuid):
    new_transaction_log = TransactionLog(
        transaction_uuid=trx_uuid, event_type=EventType.processing, event_details=None
    )

    session.add(new_transaction_log)

    return new_transaction_log


def create_settled_transaction_log(
    session: Session,
    trx_uuid,
    success: bool,
    event_details: str,
):
    new_transaction_log = TransactionLog(
        transaction_uuid=trx_uuid,
        event_type=EventType.success if success else EventType.failed,
        event_details=event_details
    )

    session.add(new_transaction_log)
    
    return new_transaction_log

