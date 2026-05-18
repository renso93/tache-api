import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# --- Configuration de la base de données de test ---
TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test) 

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- Fixture pour créer la base de données de test ---
@pytest.fixture(autouse=True)
def reset_db():
    """Reset la base de données avant chaque test"""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

# --- Fixture pour le client de test ---
@pytest.fixture
def client():
    """Fixture pour le client de test FastAPI"""
    return TestClient(app)

@pytest.fixture
def create_user(client):
    """Test de création d'un utilisateur"""
    client.post("/auth/register", json={
        "username": "testclient",
        "email": "test@gmail.com",
        "password": "123456"
        })
    return {"email": "test@gmail.com", "password": "123456"}

@pytest.fixture
def token(client, create_user):
    """Retourne un token d'authentification pour les tests"""
    response = client.post("/auth/login", data={
        "username": create_user["email"],
        "password": create_user["password"]
    })
    return response.json()["access_token"]

@pytest.fixture
def headers(token):
    """Retourne les headers d'authentification pour les tests"""
    return {"Authorization": f"Bearer {token}"}

# --- Tests autentification ---
def test_register_success(client):
    """Test de l'inscription d'un utilisateur"""
    response = client.post("/auth/register", json={
        "username": "renso",
        "email": "renso@gmail.com",
        "password": "renso123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "renso@gmail.com"
    assert response.json()["username"] == "renso"

def test_register_existing_email(client, create_user):
    """Test de l'inscription avec un email déjà existant"""
    response = client.post("/auth/register", json={
        "username": "anotheruser",
        "email": "test@gmail.com",
        "password": "renso123"
    })
    assert response.status_code == 400
    assert "Username or email already registered" in response.json()["detail"]

def test_register_password_too_short(client):
    """Test de l'inscription avec un mot de passe trop court"""
    response = client.post("/auth/register", json={
        "username": "renso",
        "email": "renso@gmail.com",
        "password": "123"
    })
    assert response.status_code == 422

def test_login_success(client, create_user):
    """Test de la connexion d'un utilisateur"""
    response = client.post("/auth/login", data={
        "username": create_user["email"],
        "password": create_user["password"]
    })
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

def test_login_password_incorrect(client, create_user):
    """Test de la connexion avec un mot de passe incorrect"""
    response = client.post("/auth/login", data={
        "username": create_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]

def test_get_user_profile(client, headers):
    """Test de l'accès au profil de l'utilisateur"""
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@gmail.com"

def test_get_user_profile_unauthorized(client):
    """Test de l'accès au profil sans token d'authentification"""
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_get_user_profile_invalid_token(client):
    """Test de l'accès au profil avec un token d'authentification invalide"""
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401

# --- Tests de gestion des tâches ---

def test_tache_create(client, headers):
    response = client.post("/taches/", json={
        "title": "Ma tâche test",
        "description": "Description test",
        "terminated": False,
        "user_id": 1
    }, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Ma tâche test"
    assert response.json()["terminated"] == False

def test_tache_list(client, headers):
    # Créer 2 tâches
    client.post("/taches/", json={"title": "Tâche 1", "user_id": 1}, headers=headers)
    client.post("/taches/", json={"title": "Tâche 2", "user_id": 1}, headers=headers)

    response = client.get("/taches/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_tache_get(client, headers):
    # Créer une tâche
    created = client.post("/taches/", json={
        "title": "Tâche test",
        "user_id": 1
    }, headers=headers)
    tache_id = created.json()["id"]

    response = client.get(f"/taches/{tache_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Tâche test"

def test_tache_update(client, headers):
    created = client.post("/taches/", json={
        "title": "Ancienne tâche",
        "user_id": 1
    }, headers=headers)
    tache_id = created.json()["id"]

    response = client.put(f"/taches/{tache_id}", json={
        "title": "Nouvelle tâche",
        "terminated": True
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Nouvelle tâche"
    assert response.json()["terminated"] == True

def test_tache_delete(client, headers):
    created = client.post("/taches/", json={
        "title": "Tâche à supprimer",
        "user_id": 1
    }, headers=headers)
    tache_id = created.json()["id"]

    response = client.delete(f"/taches/{tache_id}", headers=headers)
    assert response.status_code == 204

    # Vérifier que la tâche n'existe plus
    response = client.get(f"/taches/{tache_id}", headers=headers)
    assert response.status_code == 404

def test_tache_sans_token(client):
    response = client.get("/taches/")
    assert response.status_code == 401

def test_tache_over_user(client):
    """Un utilisateur ne peut pas accéder aux tâches d'un autre"""
    # Créer utilisateur 1
    client.post("/auth/register", json={
        "username": "user1",
        "email": "user1@gmail.com",
        "password": "test123"
    })
    token1 = client.post("/auth/login", data={
        "username": "user1@gmail.com",
        "password": "test123"
    }).json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Créer utilisateur 2
    client.post("/auth/register", json={
        "username": "user2",
        "email": "user2@gmail.com",
        "password": "test123"
    })
    token2 = client.post("/auth/login", data={
        "username": "user2@gmail.com",
        "password": "test123"
    }).json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User1 crée une tâche
    created = client.post("/taches/", json={
        "title": "Tâche privée",
        "user_id": 1
    }, headers=headers1)
    tache_id = created.json()["id"]

    # User2 essaie d'accéder à la tâche de User1
    response = client.get(f"/taches/{tache_id}", headers=headers2)
    assert response.status_code == 404
