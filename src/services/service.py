from src.models.service import Service
from sqlmodel import Session, select


def get_first_service(session: Session):
    return session.exec(select(Service).limit(1)).first()


def get_all_services(session: Session):
    return session.exec(select(Service)).all()
