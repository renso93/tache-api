from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.tache_service import create_tache, get_taches_by_user, get_tache
from app.core.security import get_current_user
from app.schemas.schemas import TacheCreate, TacheUpdate, TacheResponse
from app.models.models import User

router = APIRouter(
    prefix="/taches",
    tags=["taches"]
)

@router.post("/", response_model=TacheResponse, status_code=201)
def create_new_tache(tache_create: TacheCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Crée une nouvelle tâche pour l'utilisateur actuellement authentifié.
    Args: tache_create (TacheCreate): Les données de la tâche à créer. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée. current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: TacheResponse: La tâche créée.

    Exemple d'utilisation:
    new_tache = create_new_tache(tache_create, db, current_user)
    """    
    return create_tache(db, tache_create, current_user)

@router.get("/", response_model=List[TacheResponse])
def read_user_taches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Récupère toutes les tâches associées à l'utilisateur actuellement authentifié.
    Args: db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée. current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: List[TacheResponse]: La liste des tâches associées à l'utilisateur.

    Exemple d'utilisation:
    taches = read_user_taches(db, current_user)
    """    
    return get_taches_by_user(db, current_user)

@router.get("/{tache_id}", response_model=TacheResponse)
def read_tache(tache_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Récupère une tâche spécifique par son ID pour l'utilisateur actuellement authentifié.
    Args: tache_id (int): L'ID de la tâche à récupérer. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée. current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: TacheResponse: La tâche correspondante.

    Exemple d'utilisation:
    tache = read_tache(tache_id, db, current_user)
    """    
    return get_tache(db, tache_id, current_user)

@router.put("/{tache_id}", response_model=TacheResponse)
def update_tache(tache_id: int, tache_update: TacheUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Met à jour une tâche spécifique par son ID pour l'utilisateur actuellement authentifié.
    Args: tache_id (int): L'ID de la tâche à mettre à jour. tache_update (TacheUpdate): Les données de mise à jour de la tâche. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée. current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: TacheResponse: La tâche mise à jour.

    Exemple d'utilisation:
    updated_tache = update_tache(tache_id, tache_update, db, current_user)
    """    
    return update_tache(db, tache_id, tache_update, current_user)

@router.delete("/{tache_id}", status_code=204)
def delete_tache(tache_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Supprime une tâche spécifique par son ID pour l'utilisateur actuellement authentifié.
    Args: tache_id (int): L'ID de la tâche à supprimer. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée. current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: None

    Exemple d'utilisation:
    delete_tache(tache_id, db, current_user)
    """    
    return delete_tache(db, tache_id, current_user)

@router.post("/{tache_id}/toggle", response_model=TacheResponse)
def toggle_tache_termination(tache_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Bascule l'état de terminaison d'une tâche spécifique par son ID pour l'utilisateur actuellement authentifié.
    Args: tache_id (int): L'ID de la tâche à basculer. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée. current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: TacheResponse: La tâche avec l'état de terminaison basculé.

    Exemple d'utilisation:
    toggled_tache = toggle_tache_termination(tache_id, db, current_user)
    """    
    return toggle_tache_termination(db, tache_id, current_user)