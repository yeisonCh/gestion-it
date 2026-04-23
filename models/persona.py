from database import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
import uuid

class Persona(Base):
    __tablename__ = "personas"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    usuario = relationship("Usuario", back_populates="persona", uselist=False)
    tecnico = relationship("Tecnico", back_populates="persona", uselist=False)