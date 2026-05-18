from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # À adapter selon votre environnement
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Inclure les routes d'authentification et de gestion des tâches
app.include_router(auth_router)
app.include_router(tache_router)

# Gestionnaires d'erreurs globaux
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gère les exceptions HTTP et retourne une réponse JSON standardisée"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Gère les exceptions non-gérées et retourne une erreur générique"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "detail": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )

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