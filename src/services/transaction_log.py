from sqlmodel import Session
from src.models.transaction_log import EventType, TransactionLog


def create_processing_transaction_log(session: Session, trx_uuid):
    new_transaction_log = TransactionLog(
        transaction_uuid=trx_uuid,
        event_type=EventType.processing,
        event_details=None
     )
    
    session.add(new_transaction_log)
    
    return new_transaction_log

