from sqlalchemy.orm import Session
from repositories.tipo_activo import obtener_tipo_activo, obtener_tipo_activo_por_id, crear_tipo_activo
from schemas.tipo_activo import CrearTipoActivo
from uuid import UUID

def serice_obtener_tipo_activo(db: Session):
    return obtener_tipo_activo

def service_obtener_tipo_activo_por_id(db: Session, tipo_activo_id: UUID ):
    return obtener_tipo_activo_por_id

def service_crear_tipo_activo(db: Session, tipo_activo: CrearTipoActivo):
    return crear_tipo_activo