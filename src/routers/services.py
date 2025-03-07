from fastapi import APIRouter
from src.database import SessionDep
from src.models.service import ServicePublic
from src.services.services import get_all_services

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[ServicePublic])
def read_services(session: SessionDep):
    return get_all_services(session)
