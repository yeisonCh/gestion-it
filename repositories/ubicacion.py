# app/repositories/ubicacion.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.ubicacion import Ubicacion
from schemas.ubicacion import UbicacionCrear, UbicacionActualizar
from uuid import UUID
from typing import List, Optional

# Obtener todas las ubicaciones
def obtener_ubicaciones(db: Session) -> List[Ubicacion]:
    """Obtener todas las ubicaciones ordenadas por nombre"""
    try:
        return db.query(Ubicacion).order_by(Ubicacion.nombre).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener ubicaciones: {str(e)}")

# Obtener ubicación por ID
def obtener_ubicacion_por_id(db: Session, ubicacion_id: UUID) -> Optional[Ubicacion]:
    """Obtener una ubicación por su UUID"""
    try:
        return db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar ubicación: {str(e)}")

# Obtener ubicaciones por empresa
def obtener_ubicaciones_por_empresa(db: Session, empresa_id: UUID) -> List[Ubicacion]:
    """Obtener todas las ubicaciones de una empresa"""
    try:
        return db.query(Ubicacion).filter(Ubicacion.empresa_id == empresa_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener ubicaciones por empresa: {str(e)}")

# Crear nueva ubicación
def crear_ubicacion(db: Session, ubicacion: UbicacionCrear) -> Ubicacion:
    """Crear una nueva ubicación"""
    try:
        nueva_ubicacion = Ubicacion(
            nombre=ubicacion.nombre.upper().strip(),
            descripcion=ubicacion.descripcion.strip() if ubicacion.descripcion else None,
            empresa_id=ubicacion.empresa_id
        )
        
        db.add(nueva_ubicacion)
        db.commit()
        db.refresh(nueva_ubicacion)
        
        return nueva_ubicacion
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear ubicación: {str(e)}")

# Actualizar ubicación existente
def actualizar_ubicacion(
    db: Session, 
    ubicacion_id: UUID, 
    ubicacion_data: UbicacionActualizar
) -> Optional[Ubicacion]:
    """Actualizar una ubicación existente"""
    try:
        ubicacion = obtener_ubicacion_por_id(db, ubicacion_id)
        
        if not ubicacion:
            return None
        
        if ubicacion_data.nombre is not None:
            ubicacion.nombre = ubicacion_data.nombre.upper().strip()
        
        if ubicacion_data.descripcion is not None:
            ubicacion.descripcion = ubicacion_data.descripcion.strip() if ubicacion_data.descripcion else None
        
        if ubicacion_data.empresa_id is not None:
            ubicacion.empresa_id = ubicacion_data.empresa_id
        
        db.commit()
        db.refresh(ubicacion)
        
        return ubicacion
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar ubicación: {str(e)}")
