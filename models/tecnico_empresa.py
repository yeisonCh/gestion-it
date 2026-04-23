from database import Base
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

class TecnicoEmpresa(Base):
    __tablename__ = "tecnico_empresa"

    tecnico_id = Column(UNIQUEIDENTIFIER, ForeignKey("tecnicos.id"), nullable=False)
    empresa_id = Column(UNIQUEIDENTIFIER, ForeignKey("empresas.id"), nullable=False)

     # clave compuesta explícitamente
    __table_args__ = (
        PrimaryKeyConstraint('tecnico_id', 'empresa_id'),
    )