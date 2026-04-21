from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import User, Tache
from app.schemas.schemas import TacheCreate, TacheUpdate
from typing import List

def create_tache(db: Session, tache_create: TacheCreate, user: User) -> Tache:
    """
    Crée une nouvelle tâche dans la base de données.
    Args: db (Session): La session de base de données. tache_create (TacheCreate): Les données de la tâche à créer. user (User): L'utilisateur qui crée la tâche.
    Returns: Tache: La tâche créée.

    Exemple d'utilisation:
    new_tache = create_tache(db, tache_create, user)
    """    
    # Vérifier si l'utilisateur existe
    """ if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") """
    
    # Créer une nouvelle instance de Tache
    new_tache = Tache(
        title=tache_create.title,
        description=tache_create.description,
        terminated=tache_create.terminated,
        user_id=user.id
    )
    
    # Ajouter et committer la nouvelle instance dans la base de données
    db.add(new_tache)
    db.commit()
    db.refresh(new_tache)
    
    return new_tache

def get_taches_by_user(db: Session, user: User) -> List[Tache]:
    """
    Récupère toutes les tâches associées à un utilisateur donné.
    Args: db (Session): La session de base de données. user (User): L'utilisateur dont on veut récupérer les tâches.
    Returns: List[Tache]: La liste des tâches associées à l'utilisateur.

    Exemple d'utilisation:
    taches = get_taches_by_user(db, user)
    """    
    # Vérifier si l'utilisateur existe
    """ if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") """
    
    # Récupérer les tâches associées à l'utilisateur
    taches = db.query(Tache).filter(Tache.user_id == user.id).all()
    
    return taches

def get_tache(db: Session, tache_id: int, user: User) -> Tache:
    """
    Récupère une tâche spécifique par son ID et l'utilisateur associé.
    Args: db (Session): La session de base de données. tache_id (int): L'ID de la tâche à récupérer. user (User): L'utilisateur auquel la tâche doit être associée.
    Returns: Tache: La tâche correspondante.

    Exemple d'utilisation:
    tache = get_tache(db, tache_id, user)
    """    
    # Récupérer la tâche par ID et vérifier qu'elle appartient à l'utilisateur
    tache = db.query(Tache).filter(Tache.id == tache_id, Tache.user_id == user.id).first()
    
    if not tache:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tache not found")
    
    return tache

def update_tache(db: Session, tache_id: int, tache_update: TacheUpdate, user: User) -> Tache:
    """
    Met à jour une tâche existante dans la base de données.
    Args: db (Session): La session de base de données. tache_id (int): L'ID de la tâche à mettre à jour. tache_update (TacheUpdate): Les données de mise à jour de la tâche. user (User): L'utilisateur qui met à jour la tâche.
    Returns: Tache: La tâche mise à jour.

    Exemple d'utilisation:
    updated_tache = update_tache(db, tache_id, tache_update, user)
    """    
    # Récupérer la tâche à mettre à jour
    tache = get_tache(db, tache_id, user)
    
    if not tache:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tache not found")
    
    tache_update = tache_update.model_dump(exclude_unset=True)  # Exclure les champs non définis pour ne pas les écraser avec des valeurs par défaut   
    for key, value in tache_update.items():
        setattr(tache, key, value)


    # Mettre à jour les champs de la tâche
    """  if tache_update.title is not None:
        tache.title = tache_update.title
    if tache_update.description is not None:
        tache.description = tache_update.description
    if tache_update.terminated is not None:
        tache.terminated = tache_update.terminated """
    
    # Commit les changements dans la base de données
    db.commit()
    db.refresh(tache)
    
    return tache

def delete_tache(db: Session, tache_id: int, user: User) -> dict:
    """
    Supprime une tâche de la base de données.
    Args: db (Session): La session de base de données. tache_id (int): L'ID de la tâche à supprimer. user (User): L'utilisateur qui supprime la tâche.
    Returns: dict: Un message de confirmation.
    Exemple d'utilisation:
    delete_tache(db, tache_id, user)
    """    
    # Récupérer la tâche à supprimer
    tache = get_tache(db, tache_id, user)
    
    if not tache:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tache not found")
    
    # Supprimer la tâche de la base de données
    db.delete(tache)
    db.commit()
    return {"message": f"Tache '{tache.title}' deleted successfully"}