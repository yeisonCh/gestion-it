from database import Base
from sqlalchemy import Column, Integer, String, Date

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)