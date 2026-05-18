from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache

class Settings(BaseSettings):
    """Configuration centralisée lue depuis .env ou  variable d’environnement"""

    # === DATABASE ===
    BD_USER: str = "postgres"
    BD_PASSWORD: str = "postgres123"
    BD_HOST: str = "localhost"
    BD_NAME: str = "taches_api_db"
    BD_PORT: int = 5432

    #  === JWT ===
    SECRET_KEY: str = "your-secret-key-change-me-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # === APP ===
    APP_NAME: str = "Taches API"
    DEBUG: bool = False
    ENVIRONMENT: str = "development" # development, staging, production

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    """ class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" """

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, v):
        """Valide que SECRET_KEY a au minimum 32 caraactères"""
        if len(v) < 32:
            raise ValueError(f"SECRET_KEY must be at 32 characters long."
                             f"Current length: {len(v)}."
                             f"Please set a longer SECRET_KEY in .env or environment variables")
        return v

    @field_validator("ENVIRONMENT", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Valide que ENVIRONMENT est une valeur acceptable"""
        if v not in ["development",  "staging", "production"]:
            raise ValueError(
                f"ENVIRONMENT must be one of: development, staging, production."
                f"Got: {v}"
            )
        return v

    @property
    def database(self) -> str:
        """Construit l’URL de connexion PostgreSQL"""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def is_production(self) -> bool:
        """Vérifie si l’app est en production"""
        return self.ENVIRONMENT == "production"
        

@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance singleton de Settings (cached)"""
    return Settings()

settings = get_settings()