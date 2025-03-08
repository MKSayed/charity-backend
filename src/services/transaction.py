from src.models.transaction import POSInteractionMethod, Transaction, TransactionStatus
from sqlmodel import Session

from src.utils.geidea_api import TransactionResult


def create_processing_transaction(
    session: Session, phone_number: str, trx_amount: float, service_id: int
) -> Transaction:
    new_transaction = Transaction(
        phone_no=phone_number,
        transaction_amount=trx_amount,
        service_id=service_id,
        status=TransactionStatus.processing,
    )

    session.add(new_transaction)

    return new_transaction


def update_processing_transaction(
    processing_trx: Transaction, success: bool, trx_output: TransactionResult
):
    if success:
        if "contactless" in trx_output.html_invoice.lower():
            interaction_method = POSInteractionMethod.contactless
        else:
            interaction_method = POSInteractionMethod.dipped
        processing_trx.pos_interaction_method = interaction_method
        processing_trx.card_number = trx_output.card_number
        processing_trx.terminal_id = trx_output.terminal_id
        processing_trx.merchant_id = trx_output.merchant_id
        processing_trx.ecr_ref_no = trx_output.ecr_ref_no
        processing_trx.trx_datetime = (
            trx_output.trx_datetime if trx_output.trx_datetime else None
        )
        processing_trx.status = TransactionStatus.completed
    else:
        processing_trx.status = TransactionStatus.failed