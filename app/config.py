from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    telegram_bot_token: str = ""
    database_url: str = "sqlite:///data/medicamentos.db"
    datos_gov_dataset_id: str = "i7cb-raxc"
    datos_gov_base_url: str = "https://www.datos.gov.co/resource"
    clinical_info_path: Path = Field(default=Path("data/info_clinica.csv"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
