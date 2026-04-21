from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
#from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    """
    Hash le mot de passe en clair en utilisant bcrypt et retourne le hash résultant.
    Args: password (str): Le mot de passe en clair à hasher.
    Returns: str: Le mot de passe hashé.

    Exemple d'utilisation:
    hashed_password = hash_password("my_secure_password")
    """    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en clair correspond au mot de passe hashé.
    Args: plain_password (str): Le mot de passe en clair à vérifier. hashed_password (str): Le mot de passe hashé à comparer.
    Returns: bool: True si les mots de passe correspondent, sinon False.

    Exemple d'utilisation:
    is_valid = verify_password("my_secure_password", hashed_password)
    """    
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crée un token d'accès JWT en utilisant les données fournies et une durée d'expiration optionnelle.
    Args: data (dict): Les données à inclure dans le payload du token. expires_delta (timedelta, optional): La durée d'expiration du token. Si None, le token n'expire pas.
    Returns: str: Le token d'accès JWT généré.

    Exemple d'utilisation:
    access_token = create_access_token(data={"sub": "user_id"})
    """    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Décode un token d'accès JWT et retourne les données contenues dans le payload.
    Args: token (str): Le token d'accès JWT à décoder.
    Returns: dict: Les données contenues dans le payload du token.

    Exemple d'utilisation:
    token_data = decode_access_token(access_token)
    """    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'accès invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Récupère l'utilisateur actuel en fonction du token d'accès JWT fourni.
    Args: token (str): Le token d'accès JWT fourni dans l'en-tête Authorization. db (Session): La session de base de données pour effectuer les requêtes.
    Returns: User: L'utilisateur correspondant au token d'accès.

    Exemple d'utilisation:
    current_user = get_current_user(token, db)
    """  

    from app.models.models import User # Importation locale pour éviter les problèmes de dépendances circulaires

    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'accès invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #user = db.query(User).filter(User.email == email).first()
    #if user is None:
    #    raise HTTPException(
    #        status_code=status.HTTP_401_UNAUTHORIZED,
    #        detail="Utilisateur non trouvé",
    #        headers={"WWW-Authenticate": "Bearer"},
    #    )
    #return user