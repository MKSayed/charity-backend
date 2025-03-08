from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from src.config import settings

sqlite_file_name = settings.sqlite_file_name

sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=False)


def create_db_and_tables():
    """
    Create database file and tables only if they don't exist
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
