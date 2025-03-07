from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.database import create_db_and_tables
from src.routers import services, transactions
from src.utils.create_initial_data import create_initial_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    create_db_and_tables()
    create_initial_data()
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
