from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.models.models import Base
from app.routes.auth import router as auth_router
from app.routes.taches import router as tache_router

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tache API",
    description="API pour la gestion des tâches avec authentification JWT",
    version="1.0.0"
)

# Middleware CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines (à restreindre en production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes d'authentification et de gestion des tâches
app.include_router(auth_router)
app.include_router(tache_router)

@app.get("/")
def health_check():
    """
    Point de terminaison pour vérifier que l'API est opérationnelle.
    Returns: dict: Un message indiquant que l'API est en bonne santé.

    Exemple d'utilisation:
    response = health_check()
    """    
    return {
        "status": "success",
        "app": "Tache API",
        "version": "1.0.0",
    }