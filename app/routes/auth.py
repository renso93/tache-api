from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import register_user, authenticate_user
from app.schemas.schemas import UserCreate, UserResponse, Token
from app.core.security import get_current_user
from app.models.models import User

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Enregistre un nouvel utilisateur.
    Args: user_create (UserCreate): Les données de l'utilisateur à créer. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée.
    Returns: UserResponse: L'utilisateur créé.

    Exemple d'utilisation:
    new_user = register(user_create, db)
    """    
    return register_user(db, user_create)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authentifie un utilisateur et retourne un token d'accès.
    Args: form_data (OAuth2PasswordRequestForm, optional): Les données de connexion de l'utilisateur. db (Session, optional): La session de base de données. Par défaut, une nouvelle session est créée.
    Returns: user: L'utilisateur authentifié.

    Exemple d'utilisation:
    token = login(form_data, db)
    """    
    user = authenticate_user(db, form_data.username, form_data.password)
    #access_token = create_access_token(data={"sub": str(user.id)})
    return user

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur actuellement authentifié.
    Args: current_user (User, optional): L'utilisateur actuellement authentifié. Par défaut, l'utilisateur est récupéré à partir du token d'accès.
    Returns: UserResponse: Les informations de l'utilisateur.

    Exemple d'utilisation:
    user_info = read_current_user(current_user)
    """    
    return current_user