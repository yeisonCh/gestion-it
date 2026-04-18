from database import Base
from sqlalchemy import Column, Integer, String

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nit = Column(String(20), unique=True, nullable=False)
    direccion = Column(String(300), nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    sede = Column(String(200), nullable=True)