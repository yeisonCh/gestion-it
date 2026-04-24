# app/services/empresa.py

from sqlalchemy.orm import Session
from repositories.empresa import (
    obtener_empresas,
    obtener_empresa_por_id,
    obtener_empresa_por_nit,
    obtener_empresa_por_nombre,
    crear_empresa,
    actualizar_empresa,
    eliminar_empresa
)
from schemas.empresa import EmpresaCrear, EmpresaActualizar
from uuid import UUID
from typing import List

# Obtener todas las empresas
def service_obtener_empresas(db: Session):
    """Obtener todas las empresas"""
    return obtener_empresas(db)

# Obtener empresa por ID
def service_obtener_empresa_por_id(db: Session, empresa_id: UUID):
    """Obtener una empresa por su ID"""
    # CORREGIDO: tipo UUID en lugar de int
    return obtener_empresa_por_id(db, empresa_id)

# Crear nueva empresa (con validaciones de negocio)
def service_crear_empresa(db: Session, empresa: EmpresaCrear):
    """
    Crear una nueva empresa
    - Valida que el NIT no exista
    - Valida que el nombre no exista
    """
    # Validación: ¿Ya existe una empresa con ese NIT?
    existe_nit = obtener_empresa_por_nit(db, empresa.nit)
    if existe_nit:
        raise Exception(f"Ya existe una empresa con el NIT '{empresa.nit}'")
    
    # Validación: ¿Ya existe una empresa con ese nombre?
    existe_nombre = obtener_empresa_por_nombre(db, empresa.nombre)
    if existe_nombre:
        raise Exception(f"Ya existe una empresa con el nombre '{empresa.nombre}'")
    
    return crear_empresa(db, empresa)

# Actualizar empresa existente
def service_actualizar_empresa(
    db: Session, 
    empresa_id: UUID, 
    empresa_data: EmpresaActualizar
):
    """
    Actualizar una empresa existente
    - Valida que la empresa existe
    - Valida que el nuevo NIT no pertenezca a otra empresa
    - Valida que el nuevo nombre no pertenezca a otra empresa
    """
    # Validación 1: ¿Existe la empresa?
    existe = obtener_empresa_por_id(db, empresa_id)
    if not existe:
        raise Exception(f"Empresa con ID {empresa_id} no encontrada")
    
    # Validación 2: Si está actualizando el NIT, ¿el nuevo NIT ya existe en otra empresa?
    if empresa_data.nit:
        nit_existe = obtener_empresa_por_nit(db, empresa_data.nit)
        if nit_existe and nit_existe.id != empresa_id:
            raise Exception(f"Ya existe otra empresa con el NIT '{empresa_data.nit}'")
    
    # Validación 3: Si está actualizando el nombre, ¿el nuevo nombre ya existe en otra empresa?
    if empresa_data.nombre:
        nombre_existe = obtener_empresa_por_nombre(db, empresa_data.nombre)
        if nombre_existe and nombre_existe.id != empresa_id:
            raise Exception(f"Ya existe otra empresa con el nombre '{empresa_data.nombre}'")
    
    return actualizar_empresa(db, empresa_id, empresa_data)

# Eliminar empresa
def service_eliminar_empresa(db: Session, empresa_id: UUID):
    """
    Eliminar una empresa
    - Valida que la empresa existe
    """
    # Validación: ¿Existe la empresa?
    existe = obtener_empresa_por_id(db, empresa_id)
    if not existe:
        raise Exception(f"Empresa con ID {empresa_id} no encontrada")
    
    return eliminar_empresa(db, empresa_id)