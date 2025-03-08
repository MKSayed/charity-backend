from fastapi import APIRouter
from src.database import SessionDep
from src.models.transaction import TransactionCreate
from src.services.transaction import create_processing_transaction
from src.services.transaction_log import create_processing_transaction_log
from src.utils.geidea_api_helper import process_purchase_transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/")
def create_transaction(trx: TransactionCreate, session: SessionDep):
    processing_trx = create_processing_transaction(
        session, trx.phone_no, trx.transaction_amount, trx.service_id
    )

    processing_trx_log = create_processing_transaction_log(
        session, processing_trx.uuid
    )

    response = process_purchase_transaction(trx.transaction_amount)
    
    session.rollback()
    
    print(response)