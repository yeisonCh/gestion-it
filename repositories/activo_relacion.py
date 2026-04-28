# app/repositories/activo_relacion.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.activo_relacion import ActivoRelacion
from schemas.activo_relacion import ActivoRelacionCrear, ActivoRelacionActualizar
from uuid import UUID
from typing import List, Optional
from datetime import date

# Obtener todas las relaciones
def obtener_relaciones(db: Session) -> List[ActivoRelacion]:
    """Obtener todas las relaciones entre activos"""
    try:
        return db.query(ActivoRelacion).order_by(ActivoRelacion.fecha_asignacion.desc()).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener relaciones: {str(e)}")

# Obtener relación por ID
def obtener_relacion_por_id(db: Session, relacion_id: UUID) -> Optional[ActivoRelacion]:
    """Obtener una relación por su UUID"""
    try:
        return db.query(ActivoRelacion).filter(ActivoRelacion.id == relacion_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar relación: {str(e)}")

# Obtener relaciones por activo padre
def obtener_relaciones_por_padre(db: Session, activo_padre_id: UUID) -> List[ActivoRelacion]:
    """Obtener todas las relaciones donde el activo es padre"""
    try:
        return db.query(ActivoRelacion).filter(
            ActivoRelacion.activo_padre_id == activo_padre_id,
            ActivoRelacion.fecha_fin.is_(None)  # Solo relaciones activas
        ).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar relaciones por padre: {str(e)}")

# Obtener relaciones por activo hijo
def obtener_relaciones_por_hijo(db: Session, activo_hijo_id: UUID) -> List[ActivoRelacion]:
    """Obtener todas las relaciones donde el activo es hijo"""
    try:
        return db.query(ActivoRelacion).filter(
            ActivoRelacion.activo_hijo_id == activo_hijo_id,
            ActivoRelacion.fecha_fin.is_(None)  # Solo relaciones activas
        ).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar relaciones por hijo: {str(e)}")

# Obtener relaciones activas (sin fecha_fin)
def obtener_relaciones_activas(db: Session) -> List[ActivoRelacion]:
    """Obtener todas las relaciones activas (sin fecha de fin)"""
    try:
        return db.query(ActivoRelacion).filter(ActivoRelacion.fecha_fin.is_(None)).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener relaciones activas: {str(e)}")

# Verificar si existe relación activa entre padre e hijo
def existe_relacion_activa(db: Session, activo_padre_id: UUID, activo_hijo_id: UUID) -> bool:
    """Verificar si ya existe una relación activa entre estos dos activos"""
    try:
        relacion = db.query(ActivoRelacion).filter(
            ActivoRelacion.activo_padre_id == activo_padre_id,
            ActivoRelacion.activo_hijo_id == activo_hijo_id,
            ActivoRelacion.fecha_fin.is_(None)
        ).first()
        return relacion is not None
    except SQLAlchemyError as e:
        raise Exception(f"Error al verificar relación: {str(e)}")

# Crear nueva relación
def crear_relacion(db: Session, relacion: ActivoRelacionCrear) -> ActivoRelacion:
    """Crear una nueva relación entre activos"""
    try:
        nueva_relacion = ActivoRelacion(
            activo_padre_id=relacion.activo_padre_id,
            activo_hijo_id=relacion.activo_hijo_id,
            fecha_asignacion=relacion.fecha_asignacion,
            fecha_fin=relacion.fecha_fin,
            motivo_retiro=relacion.motivo_retiro.strip() if relacion.motivo_retiro else None
        )
        
        db.add(nueva_relacion)
        db.commit()
        db.refresh(nueva_relacion)
        
        return nueva_relacion
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear relación: {str(e)}")

# Finalizar relación (agregar fecha_fin y motivo)
def finalizar_relacion(
    db: Session, 
    relacion_id: UUID, 
    data: ActivoRelacionActualizar
) -> Optional[ActivoRelacion]:
    """Finalizar una relación existente (agregar fecha_fin y motivo)"""
    try:
        relacion = obtener_relacion_por_id(db, relacion_id)
        
        if not relacion:
            return None
        
        if relacion.fecha_fin is not None:
            raise Exception("La relación ya está finalizada")
        
        if data.fecha_fin:
            relacion.fecha_fin = data.fecha_fin
        
        if data.motivo_retiro:
            relacion.motivo_retiro = data.motivo_retiro.strip()
        
        db.commit()
        db.refresh(relacion)
        
        return relacion
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al finalizar relación: {str(e)}")