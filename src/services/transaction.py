from src.models.transaction import Transaction, TransactionStatus
from sqlmodel import Session


def create_processing_transaction(
    session: Session, phone_number: str, trx_amount: float, service_id: int
):
    return Transaction(
        phone_no=phone_number,
        transaction_amount=trx_amount,
        service_id=service_id,
        status=TransactionStatus.processing
    )
