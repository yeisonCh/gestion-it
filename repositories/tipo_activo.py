from sqlalchemy.orm import Session
from models.tipo_activo import TipoActivo
from schemas.tipo_activo import CrearTipoActivo
from uuid import UUID

def obtener_tipo_activo(db: Session):
    return db.query(TipoActivo).all()

def obtener_tipo_activo_por_id(db: Session, tipo_activo_id: UUID):
      return db.query(TipoActivo).filter(TipoActivo.id == tipo_activo_id).first()

def crear_tipo_activo(db: Session, tipo_activo: CrearTipoActivo):
     nuevo_tipo_activo = TipoActivo(
          nombre=TipoActivo.nombre
     )
     db.add(nuevo_tipo_activo)
     db.commit
     db.refresh(nuevo_tipo_activo)
     return nuevo_tipo_activo