from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    especialidad = Column(String(100), nullable=True)
    tipo = Column(String(20), nullable=False)  # interno, externo
    persona_id = Column(UNIQUEIDENTIFIER, ForeignKey("personas.id"), nullable=False)

    persona = relationship("Persona", back_populates="tecnico")
    empresas = relationship("Empresa", secondary="tecnico_empresa", back_populates="tecnicos")