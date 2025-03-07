# in order for this file to work correctly use
# "uv run -m src.utils.create_initial_data" to run it

from src.models.service import Service
from src.database import get_session, create_db_and_tables

create_db_and_tables()

services = [
  (1, "ستر وغطاء" ),
  (2, "تعليم" ),
  (3, "اطعام" ),
  (4, "زكاة" ),
  (5, "صدقات" ),
  (6, "وقف" ),
  (7, "زكاة الفطر" ),
  (8, "زكاة لاغاثة غزة" ),
  (9, "صدقات لاغاثة غزة" )
]


for session in get_session():
  for service_id, service in services:
    new_service = Service(id=service_id, name=service)
    session.add(new_service)

  session.commit()
  print("All services was created successfully")
