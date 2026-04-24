# app/repositories/tipo_activo.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.tipo_activo import TipoActivo
from schemas.tipo_activo import CrearTipoActivo, ActualizarTipoActivo
from uuid import UUID
from typing import List, Optional

def obtener_tipos_activo(db: Session) -> List[TipoActivo]:
    """Obtener todos los tipos de activo"""
    try:
        return db.query(TipoActivo).order_by(TipoActivo.nombre).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener tipos de activo: {str(e)}")

def obtener_tipo_activo_por_id(db: Session, tipo_activo_id: UUID) -> Optional[TipoActivo]:
    """Obtener un tipo de activo por su ID"""
    try:
        return db.query(TipoActivo).filter(TipoActivo.id == tipo_activo_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar tipo de activo: {str(e)}")

def obtener_tipo_activo_por_nombre(db: Session, nombre: str) -> Optional[TipoActivo]:
    """Obtener un tipo de activo por su nombre (útil para validaciones)"""
    try:
        return db.query(TipoActivo).filter(TipoActivo.nombre == nombre.upper()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por nombre: {str(e)}")

def crear_tipo_activo(db: Session, tipo_activo: CrearTipoActivo) -> TipoActivo:
    """Crear un nuevo tipo de activo"""
    try:
        # CORREGIDO: usar tipo_activo.nombre, NO TipoActivo.nombre
        nuevo_tipo_activo = TipoActivo(
            nombre=tipo_activo.nombre.upper().strip()  # Normalizar
        )
        
        db.add(nuevo_tipo_activo)
        db.commit()  # CORREGIDO: agregar paréntesis ()
        db.refresh(nuevo_tipo_activo)
        
        return nuevo_tipo_activo
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: El nombre '{tipo_activo.nombre}' ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear tipo de activo: {str(e)}")

def actualizar_tipo_activo(
    db: Session, 
    tipo_activo_id: UUID, 
    tipo_activo_data: ActualizarTipoActivo
) -> Optional[TipoActivo]:
    """Actualizar un tipo de activo existente"""
    try:
        tipo_activo = obtener_tipo_activo_por_id(db, tipo_activo_id)
        
        if not tipo_activo:
            return None
        
        # Actualizar solo si viene el campo
        if tipo_activo_data.nombre is not None:
            tipo_activo.nombre = tipo_activo_data.nombre.upper().strip()
        
        db.commit()
        db.refresh(tipo_activo)
        
        return tipo_activo
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: El nombre ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar: {str(e)}")

def eliminar_tipo_activo(db: Session, tipo_activo_id: UUID) -> bool:
    """Eliminar un tipo de activo"""
    try:
        tipo_activo = obtener_tipo_activo_por_id(db, tipo_activo_id)
        
        if not tipo_activo:
            return False
        
        db.delete(tipo_activo)
        db.commit()
        
        return True
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: No se puede eliminar porque tiene activos relacionados")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar: {str(e)}")