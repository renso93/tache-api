from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    #Base de données
    BD_USER: str = "postgres"
    BD_PASSWORD: str = "postgres123"
    BD_HOST: str = "localhost"
    BD_NAME: str = "tache_api_db"

    #JWT
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # APP
    APP_NAME: str = "Tache API"
    DEBUG: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()