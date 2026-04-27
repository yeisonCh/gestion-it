# app/services/ubicacion.py

from sqlalchemy.orm import Session
from repositories.ubicacion import (
    obtener_ubicaciones,
    obtener_ubicacion_por_id,
    obtener_ubicaciones_por_empresa,
    crear_ubicacion,
    actualizar_ubicacion
)
from repositories.empresa import obtener_empresa_por_id
from schemas.ubicacion import UbicacionCrear, UbicacionActualizar
from uuid import UUID

# Obtener todas las ubicaciones
def service_obtener_ubicaciones(db: Session):
    """Obtener todas las ubicaciones"""
    return obtener_ubicaciones(db)

# Obtener ubicación por ID
def service_obtener_ubicacion_por_id(db: Session, ubicacion_id: UUID):
    """Obtener una ubicación por su ID"""
    return obtener_ubicacion_por_id(db, ubicacion_id)

# Obtener ubicaciones por empresa
def service_obtener_ubicaciones_por_empresa(db: Session, empresa_id: UUID):
    """Obtener todas las ubicaciones de una empresa"""
    # Validar que la empresa existe
    empresa = obtener_empresa_por_id(db, empresa_id)
    if not empresa:
        raise Exception(f"La empresa con ID {empresa_id} no existe")
    
    return obtener_ubicaciones_por_empresa(db, empresa_id)

# Crear nueva ubicación
def service_crear_ubicacion(db: Session, ubicacion: UbicacionCrear):
    """Crear una nueva ubicación"""
    # Validar que la empresa existe (si se proporcionó)
    if ubicacion.empresa_id:
        empresa = obtener_empresa_por_id(db, ubicacion.empresa_id)
        if not empresa:
            raise Exception(f"La empresa con ID {ubicacion.empresa_id} no existe")
    
    return crear_ubicacion(db, ubicacion)

# Actualizar ubicación
def service_actualizar_ubicacion(
    db: Session, 
    ubicacion_id: UUID, 
    ubicacion_data: UbicacionActualizar
):
    """Actualizar una ubicación existente"""
    # Validar que la ubicación existe
    existe = obtener_ubicacion_por_id(db, ubicacion_id)
    if not existe:
        raise Exception(f"Ubicación con ID {ubicacion_id} no encontrada")
    
    # Validar que la empresa existe (si se está actualizando)
    if ubicacion_data.empresa_id:
        empresa = obtener_empresa_por_id(db, ubicacion_data.empresa_id)
        if not empresa:
            raise Exception(f"La empresa con ID {ubicacion_data.empresa_id} no existe")
    
    return actualizar_ubicacion(db, ubicacion_id, ubicacion_data)