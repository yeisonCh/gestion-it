# app/repositories/tecnico.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from models.tecnico import Tecnico
from models.tecnico_empresa import TecnicoEmpresa
from schemas.tecnico import TecnicoCrear, TecnicoActualizar
from uuid import UUID
from typing import List, Optional



# Obtener técnico por ID
def obtener_tecnico_por_id(db: Session, tecnico_id: UUID) -> Optional[Tecnico]:
    """Obtener un técnico por su UUID"""
    try:
        return db.query(Tecnico).options(
            joinedload(Tecnico.persona)
        ).filter(Tecnico.id == tecnico_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar técnico: {str(e)}")

# Obtener técnico por persona_id (una persona solo puede ser un técnico)
def obtener_tecnico_por_persona(db: Session, persona_id: UUID) -> Optional[Tecnico]:
    """Obtener un técnico por ID de persona"""
    try:
        return db.query(Tecnico).filter(Tecnico.persona_id == persona_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar técnico por persona: {str(e)}")

# Obtener técnicos por tipo
def obtener_tecnicos_por_tipo(db: Session, tipo: str) -> List[Tecnico]:
    """Obtener técnicos filtrados por tipo (interno/externo)"""
    try:
        return db.query(Tecnico).filter(Tecnico.tipo == tipo.lower()).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar técnicos por tipo: {str(e)}")

# Obtener técnicos por empresa
def obtener_tecnicos_por_empresa(db: Session, empresa_id: UUID) -> List[Tecnico]:
    """Obtener técnicos que pertenecen a una empresa"""
    try:
        return db.query(Tecnico).join(
            TecnicoEmpresa, Tecnico.id == TecnicoEmpresa.tecnico_id
        ).filter(TecnicoEmpresa.empresa_id == empresa_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar técnicos por empresa: {str(e)}")

# Crear nuevo técnico
def crear_tecnico(db: Session, tecnico: TecnicoCrear) -> Tecnico:
    """Crear un nuevo técnico"""
    try:
        nuevo_tecnico = Tecnico(
            especialidad=tecnico.especialidad.strip() if tecnico.especialidad else None,
            tipo=tecnico.tipo.lower().strip(),
            persona_id=tecnico.persona_id
        )
        
        db.add(nuevo_tecnico)
        db.flush()  # Para obtener el ID del técnico antes de commit
        
        # Agregar relaciones con empresas si existen
        if tecnico.empresas_ids:
            for empresa_id in tecnico.empresas_ids:
                relacion = TecnicoEmpresa(
                    tecnico_id=nuevo_tecnico.id,
                    empresa_id=empresa_id
                )
                db.add(relacion)
        
        db.commit()
        db.refresh(nuevo_tecnico)
        
        return nuevo_tecnico
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear técnico: {str(e)}")

# Actualizar técnico existente
def actualizar_tecnico(
    db: Session, 
    tecnico_id: UUID, 
    tecnico_data: TecnicoActualizar
) -> Optional[Tecnico]:
    """Actualizar un técnico existente"""
    try:
        tecnico = obtener_tecnico_por_id(db, tecnico_id)
        
        if not tecnico:
            return None
        
        # Actualizar campos básicos
        if tecnico_data.especialidad is not None:
            tecnico.especialidad = tecnico_data.especialidad.strip() if tecnico_data.especialidad else None
        
        if tecnico_data.tipo is not None:
            tecnico.tipo = tecnico_data.tipo.lower().strip()
        
        if tecnico_data.persona_id is not None:
            tecnico.persona_id = tecnico_data.persona_id
        
        # Actualizar relaciones con empresas si se enviaron
        if tecnico_data.empresas_ids is not None:
            # Eliminar relaciones existentes
            db.query(TecnicoEmpresa).filter(TecnicoEmpresa.tecnico_id == tecnico_id).delete()
            
            # Agregar nuevas relaciones
            for empresa_id in tecnico_data.empresas_ids:
                relacion = TecnicoEmpresa(
                    tecnico_id=tecnico_id,
                    empresa_id=empresa_id
                )
                db.add(relacion)
        
        db.commit()
        db.refresh(tecnico)
        
        return tecnico
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar técnico: {str(e)}")