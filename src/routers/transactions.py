from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/")
def create_transaction(body: dict):
    pass
