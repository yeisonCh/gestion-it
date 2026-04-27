# app/services/activo.py

from sqlalchemy.orm import Session
from repositories.activo import (
    obtener_activos,
    obtener_activo_por_id,
    obtener_activo_por_serial,
    obtener_activos_por_tipo,
    obtener_activos_por_empresa,
    obtener_activos_por_estado,
    crear_activo,
    actualizar_activo,
    eliminar_activo
)
from repositories.tipo_activo import obtener_tipo_activo_por_id
from repositories.empresa import obtener_empresa_por_id
from repositories.usuario import obtener_usuario_por_id  # Asumiendo que existe
from schemas.activo import ActivoCrear, ActivoActualizar
from uuid import UUID
from typing import List

# Obtener todos los activos
def service_obtener_activos(db: Session):
    """Obtener todos los activos"""
    return obtener_activos(db)

# Obtener activo por ID
def service_obtener_activo_por_id(db: Session, activo_id: UUID):
    """Obtener un activo por su ID"""
    return obtener_activo_por_id(db, activo_id)

# Obtener activos por tipo
def service_obtener_activos_por_tipo(db: Session, tipo_activo_id: UUID):
    """Obtener activos filtrados por tipo de activo"""
    return obtener_activos_por_tipo(db, tipo_activo_id)

# Obtener activos por empresa
def service_obtener_activos_por_empresa(db: Session, empresa_id: UUID):
    """Obtener activos filtrados por empresa"""
    return obtener_activos_por_empresa(db, empresa_id)

# Obtener activos por estado
def service_obtener_activos_por_estado(db: Session, estado: str):
    """Obtener activos filtrados por estado"""
    return obtener_activos_por_estado(db, estado)

# Crear nuevo activo (con validaciones de negocio)
def service_crear_activo(db: Session, activo: ActivoCrear):
    """
    Crear un nuevo activo
    - Valida que el serial no exista
    - Valida que el tipo_activo_id exista
    - Valida que la empresa_id exista
    - Valida que el usuario_responsable_id exista (si se proporciona)
    """
    # Validación 1: ¿Ya existe un activo con ese serial?
    existe_serial = obtener_activo_por_serial(db, activo.serial)
    if existe_serial:
        raise Exception(f"Ya existe un activo con el serial '{activo.serial}'")
    
    # Validación 2: ¿Existe el tipo de activo?
    tipo_activo = obtener_tipo_activo_por_id(db, activo.tipo_activo_id)
    if not tipo_activo:
        raise Exception(f"El tipo de activo con ID {activo.tipo_activo_id} no existe")
    
    # Validación 3: ¿Existe la empresa?
    empresa = obtener_empresa_por_id(db, activo.empresa_id)
    if not empresa:
        raise Exception(f"La empresa con ID {activo.empresa_id} no existe")
    
    # Validación 4: Si tiene usuario responsable, ¿existe?
    if activo.usuario_responsable_id:
        usuario = obtener_usuario_por_id(db, activo.usuario_responsable_id)
        if not usuario:
            raise Exception(f"El usuario con ID {activo.usuario_responsable_id} no existe")
    
    return crear_activo(db, activo)

# Actualizar activo existente
def service_actualizar_activo(
    db: Session, 
    activo_id: UUID, 
    activo_data: ActivoActualizar
):
    """
    Actualizar un activo existente
    - Valida que el activo existe
    - Valida que el nuevo serial no pertenezca a otro activo
    - Valida que el tipo_activo_id exista (si se actualiza)
    - Valida que la empresa_id exista (si se actualiza)
    - Valida que el usuario_responsable_id exista (si se actualiza)
    """
    # Validación 1: ¿Existe el activo?
    existe = obtener_activo_por_id(db, activo_id)
    if not existe:
        raise Exception(f"Activo con ID {activo_id} no encontrado")
    
    # Validación 2: Si está actualizando el serial, ¿el nuevo serial ya existe en otro activo?
    if activo_data.serial:
        serial_existe = obtener_activo_por_serial(db, activo_data.serial)
        if serial_existe and serial_existe.id != activo_id:
            raise Exception(f"Ya existe otro activo con el serial '{activo_data.serial}'")
    
    # Validación 3: Si está actualizando tipo_activo_id, ¿existe?
    if activo_data.tipo_activo_id:
        tipo_activo = obtener_tipo_activo_por_id(db, activo_data.tipo_activo_id)
        if not tipo_activo:
            raise Exception(f"El tipo de activo con ID {activo_data.tipo_activo_id} no existe")
    
    # Validación 4: Si está actualizando empresa_id, ¿existe?
    if activo_data.empresa_id:
        empresa = obtener_empresa_por_id(db, activo_data.empresa_id)
        if not empresa:
            raise Exception(f"La empresa con ID {activo_data.empresa_id} no existe")
    
    # Validación 5: Si está actualizando usuario_responsable_id, ¿existe?
    if activo_data.usuario_responsable_id:
        usuario = obtener_usuario_por_id(db, activo_data.usuario_responsable_id)
        if not usuario:
            raise Exception(f"El usuario con ID {activo_data.usuario_responsable_id} no existe")
    
    return actualizar_activo(db, activo_id, activo_data)

# Eliminar activo
def service_eliminar_activo(db: Session, activo_id: UUID):
    """
    Eliminar un activo
    - Valida que el activo existe
    """
    # Validación: ¿Existe el activo?
    existe = obtener_activo_por_id(db, activo_id)
    if not existe:
        raise Exception(f"Activo con ID {activo_id} no encontrado")
    
    return eliminar_activo(db, activo_id)