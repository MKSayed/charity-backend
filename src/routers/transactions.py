from fastapi import APIRouter
from src.database import SessionDep
from src.models.transaction import (
    TransactionCreate,
    TransactionPublic,
)
from src.services.transaction import (
    create_processing_transaction,
    update_processing_transaction,
)
from src.services.transaction_log import (
    create_processing_transaction_log,
    create_settled_transaction_log,
)
from src.utils.geidea_api_helper import process_purchase_transaction


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionPublic)
def create_transaction(trx: TransactionCreate, session: SessionDep):
    processing_trx = create_processing_transaction(
        session, trx.phone_no, trx.transaction_amount, trx.service_id
    )

    processing_trx_log = create_processing_transaction_log(session, processing_trx.uuid)

    session.commit()
    success, response = process_purchase_transaction(
        trx.transaction_amount, "0000000000000001"
    )

    create_settled_transaction_log(
        session, processing_trx.uuid, success, response.response_message
    )

    update_processing_transaction(processing_trx, success, response)  # pyright: ignore # Handled correctly inside

    session.commit()

    return processing_trx
