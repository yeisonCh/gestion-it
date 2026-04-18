from database import Base
from sqlalchemy import Column, Integer, ForeignKey

class TecnicoEmpresa(Base):
    __tablename__ = "tecnico_empresa"

    id = Column(Integer, primary_key=True, index=True)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)