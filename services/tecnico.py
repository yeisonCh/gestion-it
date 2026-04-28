# app/services/tecnico.py

from sqlalchemy.orm import Session
from repositories.tecnico import (
    obtener_tecnico_por_id,
    obtener_tecnico_por_persona,
    obtener_tecnicos_por_tipo,
    obtener_tecnicos_por_empresa,
    crear_tecnico,
    actualizar_tecnico
)
from repositories.persona import obtener_persona_por_id
from repositories.empresa import obtener_empresa_por_id
from schemas.tecnico import TecnicoCrear, TecnicoActualizar
from uuid import UUID


# Obtener técnico por ID
def service_obtener_tecnico_por_id(db: Session, tecnico_id: UUID):
    """Obtener un técnico por su ID"""
    return obtener_tecnico_por_id(db, tecnico_id)

# Obtener técnicos por tipo
def service_obtener_tecnicos_por_tipo(db: Session, tipo: str):
    """Obtener técnicos filtrados por tipo"""
    return obtener_tecnicos_por_tipo(db, tipo)

# Obtener técnicos por empresa
def service_obtener_tecnicos_por_empresa(db: Session, empresa_id: UUID):
    """Obtener técnicos que pertenecen a una empresa"""
    # Validar que la empresa existe
    empresa = obtener_empresa_por_id(db, empresa_id)
    if not empresa:
        raise Exception(f"La empresa con ID {empresa_id} no existe")
    
    return obtener_tecnicos_por_empresa(db, empresa_id)

# Crear nuevo técnico
def service_crear_tecnico(db: Session, tecnico: TecnicoCrear):
    """Crear un nuevo técnico"""
    # Validar que la persona existe
    persona = obtener_persona_por_id(db, tecnico.persona_id)
    if not persona:
        raise Exception(f"La persona con ID {tecnico.persona_id} no existe")
    
    # Validar que la persona no sea ya un técnico
    existe = obtener_tecnico_por_persona(db, tecnico.persona_id)
    if existe:
        raise Exception(f"La persona ya está registrada como técnico")
    
    # Validar que las empresas existen
    if tecnico.empresas_ids:
        for empresa_id in tecnico.empresas_ids:
            empresa = obtener_empresa_por_id(db, empresa_id)
            if not empresa:
                raise Exception(f"La empresa con ID {empresa_id} no existe")
    
    return crear_tecnico(db, tecnico)

# Actualizar técnico
def service_actualizar_tecnico(
    db: Session, 
    tecnico_id: UUID, 
    tecnico_data: TecnicoActualizar
):
    """Actualizar un técnico existente"""
    # Validar que el técnico existe
    existe = obtener_tecnico_por_id(db, tecnico_id)
    if not existe:
        raise Exception(f"Técnico con ID {tecnico_id} no encontrado")
    
    # Validar que la persona existe (si se actualiza)
    if tecnico_data.persona_id:
        persona = obtener_persona_por_id(db, tecnico_data.persona_id)
        if not persona:
            raise Exception(f"La persona con ID {tecnico_data.persona_id} no existe")
        
        # Validar que esa persona no sea ya otro técnico
        otro_tecnico = obtener_tecnico_por_persona(db, tecnico_data.persona_id)
        if otro_tecnico and otro_tecnico.id != tecnico_id:
            raise Exception(f"La persona ya está registrada como técnico")
    
    # Validar que las empresas existen (si se actualizan)
    if tecnico_data.empresas_ids:
        for empresa_id in tecnico_data.empresas_ids:
            empresa = obtener_empresa_por_id(db, empresa_id)
            if not empresa:
                raise Exception(f"La empresa con ID {empresa_id} no existe")
    
    return actualizar_tecnico(db, tecnico_id, tecnico_data)