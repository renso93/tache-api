from sqlalchemy.orm import relationship
from sqlalchemy import (Column, 
                        Integer,
                        DateTime,
                        Boolean, 
                        String, 
                        ForeignKey)
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    taches = relationship("Tache", back_populates="proprietaire")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
class Tache(Base):
    __tablename__ = "taches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True, default="")
    terminated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Foreign key (clé étrangère) pour lier la tâche à un utilisateur (propriétaire)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Relation pour accéder à l'utilisateur propriétaire de la tâche et pour que l'utilisateur puisse accéder à ses tâches
    proprietaire = relationship("User", back_populates="taches")

    def __repr__(self):
        return f"<Tache(id={self.id}, title='{self.title}', user_id={self.user_id}, terminated={self.terminated})>"