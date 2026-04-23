from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship 
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

import uuid

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(200), nullable=False)
    nit = Column(String(20), unique=True, nullable=False)
    direccion = Column(String(300), nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    sede = Column(String(200), nullable=True)

    usuarios = relationship("Usuario", back_populates="empresa")
    tecnicos = relationship("Tecnico", secondary="tecnico_empresa", back_populates="empresas")