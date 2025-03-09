import logging
import multiprocessing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import uvicorn
from src.database import create_db_and_tables
from src.routers import services, transactions
from src.utils.create_initial_data import create_initial_data
from src.utils.my_logger import control_uvicorn_loggers, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    create_db_and_tables()
    setup_logging()
    create_initial_data()
    control_uvicorn_loggers()
    yield
    # on shutdown
    pass


app = FastAPI(title="bait-al-zakat", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router)
app.include_router(transactions.router)




if __name__ == "__main__":
    multiprocessing.freeze_support()  # To prevent possible recursions with multiple workers
    uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level=logging.WARNING)