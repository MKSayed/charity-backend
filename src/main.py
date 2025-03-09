import copy 
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
    create_initial_data()
    setup_logging()
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
    
    # Remove uvicorn logging handlers
    from uvicorn.config import LOGGING_CONFIG
    import sys
    if getattr(sys, 'frozen', False):
        # Make a deep copy of the logging config
        custom_logging = copy.deepcopy(LOGGING_CONFIG)
        
        # Replace the problematic formatter with a simple one
        custom_logging["formatters"] = {
            "default": {
                "format": "%(levelname)s: %(message)s",
            },
            "access": {
                "format": "%(levelname)s: %(message)s",
            },
        }
        
        # Make sure all handlers use our simple formatters
        for handler_name in custom_logging["handlers"]:
            if "formatter" in custom_logging["handlers"][handler_name]:
                if custom_logging["handlers"][handler_name]["formatter"] not in custom_logging["formatters"]:
                    custom_logging["handlers"][handler_name]["formatter"] = "default"

            

    uvicorn.run(app=app, host="0.0.0.0", port=8000, log_config=custom_logging) # type: ignore
