# app/repositories/activo.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.activo import Activo
from models.tipo_activo import TipoActivo
from models.empresa import Empresa
from models.usuario import Usuario
from schemas.activo import ActivoCrear, ActivoActualizar
from uuid import UUID
from typing import List, Optional

# Obtener todos los activos (con relaciones para evitar N+1 queries)
def obtener_activos(db: Session) -> List[Activo]:
    """Obtener todos los activos ordenados por serial"""
    try:
        return db.query(Activo).options(
            joinedload(Activo.tipo_activo),
            joinedload(Activo.empresa),
            joinedload(Activo.usuario_responsable)
        ).order_by(Activo.serial).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener activos: {str(e)}")

# Obtener activo por ID
def obtener_activo_por_id(db: Session, activo_id: UUID) -> Optional[Activo]:
    """Obtener un activo por su UUID con sus relaciones"""
    try:
        return db.query(Activo).options(
            joinedload(Activo.tipo_activo),
            joinedload(Activo.empresa),
            joinedload(Activo.usuario_responsable)
        ).filter(Activo.id == activo_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar activo: {str(e)}")

# Obtener activo por serial (para validar unicidad)
def obtener_activo_por_serial(db: Session, serial: str) -> Optional[Activo]:
    """Obtener un activo por su serial"""
    try:
        return db.query(Activo).filter(Activo.serial == serial.upper().strip()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por serial: {str(e)}")

# Obtener activos por tipo de activo
def obtener_activos_por_tipo(db: Session, tipo_activo_id: UUID) -> List[Activo]:
    """Obtener todos los activos de un tipo específico"""
    try:
        return db.query(Activo).filter(Activo.tipo_activo_id == tipo_activo_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar activos por tipo: {str(e)}")

# Obtener activos por empresa
def obtener_activos_por_empresa(db: Session, empresa_id: UUID) -> List[Activo]:
    """Obtener todos los activos de una empresa específica"""
    try:
        return db.query(Activo).filter(Activo.empresa_id == empresa_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar activos por empresa: {str(e)}")

# Obtener activos por estado
def obtener_activos_por_estado(db: Session, estado: str) -> List[Activo]:
    """Obtener todos los activos con un estado específico"""
    try:
        return db.query(Activo).filter(Activo.estado == estado).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar activos por estado: {str(e)}")

# Crear nuevo activo
def crear_activo(db: Session, activo: ActivoCrear) -> Activo:
    """Crear un nuevo activo"""
    try:
        nuevo_activo = Activo(
            serial=activo.serial.upper().strip(),
            nombre=activo.nombre.strip().title() if activo.nombre else None,
            marca=activo.marca.strip().title() if activo.marca else None,
            modelo=activo.modelo.strip() if activo.modelo else None,
            fecha_compra=activo.fecha_compra,
            estado=activo.estado.value,  # Enum a string
            tipo_activo_id=activo.tipo_activo_id,
            empresa_id=activo.empresa_id,
            usuario_responsable_id=activo.usuario_responsable_id
        )
        
        db.add(nuevo_activo)
        db.commit()
        db.refresh(nuevo_activo)
        
        return nuevo_activo
        
    except IntegrityError as e:
        db.rollback()
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            raise Exception(f"Error: Ya existe un activo con el serial '{activo.serial}'")
        raise Exception(f"Error de integridad al crear activo: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear activo: {str(e)}")

# Actualizar activo existente
def actualizar_activo(
    db: Session, 
    activo_id: UUID, 
    activo_data: ActivoActualizar
) -> Optional[Activo]:
    """Actualizar un activo existente"""
    try:
        activo = obtener_activo_por_id(db, activo_id)
        
        if not activo:
            return None
        
        # Actualizar solo los campos que vienen en la petición
        if activo_data.serial is not None:
            activo.serial = activo_data.serial.upper().strip()
        
        if activo_data.nombre is not None:
            activo.nombre = activo_data.nombre.strip().title() if activo_data.nombre else None
        
        if activo_data.marca is not None:
            activo.marca = activo_data.marca.strip().title() if activo_data.marca else None
        
        if activo_data.modelo is not None:
            activo.modelo = activo_data.modelo.strip() if activo_data.modelo else None
        
        if activo_data.fecha_compra is not None:
            activo.fecha_compra = activo_data.fecha_compra
        
        if activo_data.estado is not None:
            activo.estado = activo_data.estado.value
        
        if activo_data.tipo_activo_id is not None:
            activo.tipo_activo_id = activo_data.tipo_activo_id
        
        if activo_data.empresa_id is not None:
            activo.empresa_id = activo_data.empresa_id
        
        if activo_data.usuario_responsable_id is not None:
            activo.usuario_responsable_id = activo_data.usuario_responsable_id
        
        db.commit()
        db.refresh(activo)
        
        return activo
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: Ya existe otro activo con ese serial")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar activo: {str(e)}")

# Eliminar activo
def eliminar_activo(db: Session, activo_id: UUID) -> bool:
    """Eliminar un activo"""
    try:
        activo = obtener_activo_por_id(db, activo_id)
        
        if not activo:
            return False
        
        db.delete(activo)
        db.commit()
        
        return True
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: No se puede eliminar el activo porque tiene registros relacionados")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar activo: {str(e)}")