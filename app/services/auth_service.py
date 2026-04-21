from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import or_
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

def register_user(db: Session, user_create: UserCreate) -> User:
    """
    Enregistre un nouvel utilisateur dans la base de données.
    Args: db (Session): La session de base de données. user_create (UserCreate): Les données de l'utilisateur à créer.
    Returns: User: L'utilisateur créé.

    Exemple d'utilisation:
    new_user = register_user(db, user_create)
    """    
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter((User.username == user_create.username) | (User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")
    
    # Hasher le mot de passe
    hashed_password = hash_password(user_create.hashed_password)
    
    # Créer une nouvelle instance de User
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_password
    )
    
    # Ajouter et committer la nouvelle instance dans la base de données
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Authentifie un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.
    Args: db (Session): La session de base de données. username (str): Le nom d'utilisateur de l'utilisateur. password (str): Le mot de passe en clair de l'utilisateur.
    Returns: User: L'utilisateur authentifié.

    Exemple d'utilisation:
    authenticated_user = authenticate_user(db, "username", "password")
    """
    # Rechercher l'utilisateur par nom d'utilisateur ou email    
    user = db.query(User).filter(
        or_(User.username == username,
            User.email == username)
    ).first()
    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    return user

def create_user_access_token(user: User) -> str:
    """
    Crée un token d'accès JWT pour un utilisateur donné.
    Args: user (User): L'utilisateur pour lequel créer le token d'accès.
    Returns: str: Le token d'accès JWT généré.

    Exemple d'utilisation:
    access_token = create_user_access_token(user)
    """    
    access_token = create_access_token(data={"sub": user.email})
    return access_token

def get_user_from_token(db: Session, token: str) -> User:
    """
    Récupère un utilisateur à partir d'un token d'accès JWT.
    Args: db (Session): La session de base de données. token (str): Le token d'accès JWT.
    Returns: User: L'utilisateur correspondant au token d'accès.

    Exemple d'utilisation:
    user = get_user_from_token(db, access_token)
    """    
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))