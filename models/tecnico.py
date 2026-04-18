from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    especialidad = Column(String(100), nullable=True)
    tipo = Column(String(20), nullable=False)  # interno, externo
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)

    persona = relationship("Persona")
    empresas = relationship("Empresa", secondary="tecnico_empresa")