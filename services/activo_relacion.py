# app/services/activo_relacion.py

from sqlalchemy.orm import Session
from repositories.activo_relacion import (
    obtener_relaciones,
    obtener_relacion_por_id,
    obtener_relaciones_por_padre,
    obtener_relaciones_por_hijo,
    obtener_relaciones_activas,
    existe_relacion_activa,
    crear_relacion,
    finalizar_relacion
)
from repositories.activo import obtener_activo_por_id
from schemas.activo_relacion import ActivoRelacionCrear, ActivoRelacionActualizar
from uuid import UUID

# Obtener todas las relaciones
def service_obtener_relaciones(db: Session):
    """Obtener todas las relaciones entre activos"""
    return obtener_relaciones(db)

# Obtener relación por ID
def service_obtener_relacion_por_id(db: Session, relacion_id: UUID):
    """Obtener una relación por su ID"""
    return obtener_relacion_por_id(db, relacion_id)

# Obtener relaciones por activo padre
def service_obtener_relaciones_por_padre(db: Session, activo_padre_id: UUID):
    """Obtener relaciones donde el activo es padre"""
    # Validar que el activo padre existe
    activo = obtener_activo_por_id(db, activo_padre_id)
    if not activo:
        raise Exception(f"El activo padre con ID {activo_padre_id} no existe")
    
    return obtener_relaciones_por_padre(db, activo_padre_id)

# Obtener relaciones por activo hijo
def service_obtener_relaciones_por_hijo(db: Session, activo_hijo_id: UUID):
    """Obtener relaciones donde el activo es hijo"""
    # Validar que el activo hijo existe
    activo = obtener_activo_por_id(db, activo_hijo_id)
    if not activo:
        raise Exception(f"El activo hijo con ID {activo_hijo_id} no existe")
    
    return obtener_relaciones_por_hijo(db, activo_hijo_id)

# Obtener relaciones activas
def service_obtener_relaciones_activas(db: Session):
    """Obtener todas las relaciones activas (sin fecha_fin)"""
    return obtener_relaciones_activas(db)

# Crear nueva relación
def service_crear_relacion(db: Session, relacion: ActivoRelacionCrear):
    """Crear una nueva relación entre activos"""
    # Validación 1: ¿Existe el activo padre?
    activo_padre = obtener_activo_por_id(db, relacion.activo_padre_id)
    if not activo_padre:
        raise Exception(f"El activo padre con ID {relacion.activo_padre_id} no existe")
    
    # Validación 2: ¿Existe el activo hijo?
    activo_hijo = obtener_activo_por_id(db, relacion.activo_hijo_id)
    if not activo_hijo:
        raise Exception(f"El activo hijo con ID {relacion.activo_hijo_id} no existe")
    
    # Validación 3: No relacionar un activo consigo mismo
    if relacion.activo_padre_id == relacion.activo_hijo_id:
        raise Exception("No se puede relacionar un activo consigo mismo")
    
    # Validación 4: ¿Ya existe una relación activa entre estos dos activos?
    existe = existe_relacion_activa(db, relacion.activo_padre_id, relacion.activo_hijo_id)
    if existe:
        raise Exception("Ya existe una relación activa entre estos dos activos")
    
    return crear_relacion(db, relacion)

# Finalizar relación
def service_finalizar_relacion(
    db: Session, 
    relacion_id: UUID, 
    data: ActivoRelacionActualizar
):
    """Finalizar una relación existente"""
    # Validar que la relación existe
    relacion = obtener_relacion_por_id(db, relacion_id)
    if not relacion:
        raise Exception(f"Relación con ID {relacion_id} no encontrada")
    
    # Validar que no esté ya finalizada
    if relacion.fecha_fin:
        raise Exception("La relación ya está finalizada")
    
    return finalizar_relacion(db, relacion_id, data)