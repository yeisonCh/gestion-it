from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)  # admin, operativo
    habilitado = Column(Boolean, default=True)
    
    persona_id = Column(UNIQUEIDENTIFIER, ForeignKey("personas.id"), nullable=False)
    empresa_id = Column(UNIQUEIDENTIFIER, ForeignKey("empresas.id"), nullable=False)

    persona = relationship("Persona", back_populates="usuario")
    empresa = relationship("Empresa", back_populates="usuarios")