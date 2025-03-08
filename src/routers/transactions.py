from fastapi import APIRouter
from src.database import SessionDep
from src.models.transaction import TransactionCreate
from src.services.transaction import create_processing_transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/")
def create_transaction(trx: TransactionCreate, session: SessionDep):
    create_processing_transaction(
        session, trx.phone_no, trx.transaction_amount, trx.service_id
    )
    
