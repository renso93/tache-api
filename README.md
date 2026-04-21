# Tache API 🚀

API REST professionnelle de gestion de tâches.

## Stack technique
- **Framework** : FastAPI
- **Base de données** : PostgreSQL + SQLAlchemy
- **Auth** : JWT
- **Validation** : Pydantic v2
- **Tests** : pytest
- **DevOps** : Docker

## Structure du projet
\```
app/
├── core/       → configuration, sécurité, base de données
├── models/     → tables SQLAlchemy
├── schemas/    → validation Pydantic
├── routes/     → endpoints HTTP
└── services/   → logique métier
\```

## Installation

\```bash
# Cloner le projet
git clone https://github.com/renso93/tache-api.git
cd tache-api

# Créer l'environnement virtuel
python -m venv .venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate       # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Remplis .env avec tes valeurs

# Lancer l'API
uvicorn app.main:app --reload
\```

## Documentation API
http://127.0.0.1:8000/docs