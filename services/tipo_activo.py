# app/services/tipo_activo.py

from sqlalchemy.orm import Session
from repositories.tipo_activo import (
    obtener_tipos_activo,
    obtener_tipo_activo_por_id,
    obtener_tipo_activo_por_nombre,
    crear_tipo_activo,
    actualizar_tipo_activo,
    eliminar_tipo_activo
)
from schemas.tipo_activo import CrearTipoActivo, ActualizarTipoActivo
from uuid import UUID
from typing import List

# Obtener todos los tipos de activo
def service_obtener_tipos_activo(db: Session):
    return obtener_tipos_activo(db)

# Obtener un tipo de activo por ID
def service_obtener_tipo_activo_por_id(db: Session, tipo_activo_id: UUID):
    return obtener_tipo_activo_por_id(db, tipo_activo_id)

# Crear un nuevo tipo de activo (con validación)
def service_crear_tipo_activo(db: Session, tipo_activo: CrearTipoActivo):
    # ¿Ya existe un tipo con ese nombre?
    existe = obtener_tipo_activo_por_nombre(db, tipo_activo.nombre)
    
    if existe:
        raise Exception(f"El tipo de activo '{tipo_activo.nombre}' ya existe")
    
    # CORREGIDO: Pasar los parámetros correctamente
    return crear_tipo_activo(db, tipo_activo)

# Actualizar un tipo de activo existente
def service_actualizar_tipo_activo(
    db: Session, 
    tipo_activo_id: UUID, 
    tipo_activo_data: ActualizarTipoActivo
):
    # Validación 1: ¿Existe el registro?
    existe = obtener_tipo_activo_por_id(db, tipo_activo_id)
    if not existe:
        raise Exception(f"Tipo de activo con ID {tipo_activo_id} no encontrado")
    
    # Validación 2: Si está cambiando el nombre, ¿el nuevo nombre ya existe?
    if tipo_activo_data.nombre:
        nombre_existe = obtener_tipo_activo_por_nombre(db, tipo_activo_data.nombre)
        if nombre_existe and nombre_existe.id != tipo_activo_id:
            raise Exception(f"El tipo de activo '{tipo_activo_data.nombre}' ya existe")
    
    return actualizar_tipo_activo(db, tipo_activo_id, tipo_activo_data)

# Eliminar un tipo de activo
def service_eliminar_tipo_activo(db: Session, tipo_activo_id: UUID):
    # Validación: ¿Existe el registro?
    existe = obtener_tipo_activo_por_id(db, tipo_activo_id)
    if not existe:
        raise Exception(f"Tipo de activo con ID {tipo_activo_id} no encontrado")
    
    # Validación adicional: ¿Tiene activos relacionados? (lo maneja el repositorio)
    return eliminar_tipo_activo(db, tipo_activo_id)