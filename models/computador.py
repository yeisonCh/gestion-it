from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Computador(Base):
    __tablename__ = "computadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    marca = Column(String(100))
    serial = Column(String(100), unique=True)
    fecha_registro = Column(DateTime, default=datetime.now)