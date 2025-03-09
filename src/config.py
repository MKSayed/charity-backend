from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_file_name: str
    pos_comport: int
    transaction_timeout_in_secs: int
    kiosk_id: int


settings = Settings(_env_file=".config")  # pyright: ignore attributes are not optional but they'll be loaded from .env file
