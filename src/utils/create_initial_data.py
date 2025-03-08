from src.models.service import Service
from src.database import get_session
from src.services.service import get_first_service
from src.utils.my_logger import logger

services = [
    (1, "ستر وغطاء"),
    (2, "تعليم"),
    (3, "اطعام"),
    (4, "زكاة"),
    (5, "صدقات"),
    (6, "وقف"),
    (7, "زكاة الفطر"),
    (8, "زكاة لاغاثة غزة"),
    (9, "صدقات لاغاثة غزة"),
]


def create_initial_data():
    logger.warning("Attempting to save initial services to the database...")
    for session in get_session():
        first_service = get_first_service(session)
        if not first_service:
            for service_id, service in services:
                new_service = Service(id=service_id, name=service)
                session.add(new_service)
            session.commit()
            logger.warning("All services was created successfully")
        else:
            logger.warning("Services were previously initialized")
