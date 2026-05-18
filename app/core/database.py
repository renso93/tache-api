from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import URL
from urllib.parse import quote_plus
from app.core.config import settings

def get_database_url():
    return URL.create(
        drivername="postgresql+psycopg2",
        username=quote_plus(settings.BD_USER),
        password=quote_plus(settings.BD_PASSWORD),
        host=settings.BD_HOST,
        database=quote_plus(settings.BD_NAME)
    )

engine = create_engine(
    get_database_url(),
    pool_pre_ping=True, # Vérifie la connexion avant de l'utiliser
    pool_size=5, # Nombre de connexions à maintenir dans le pool
    max_overflow=10, # Nombre de connexions supplémentaires autorisées au-delà de pool_size
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()