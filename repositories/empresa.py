# app/repositories/empresa.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.empresa import Empresa
from schemas.empresa import EmpresaCrear, EmpresaActualizar
from uuid import UUID
from typing import List, Optional

# Obtener todas las empresas
def obtener_empresas(db: Session) -> List[Empresa]:
    """Obtener todas las empresas ordenadas por nombre"""
    try:
        return db.query(Empresa).order_by(Empresa.nombre).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener empresas: {str(e)}")

# Obtener empresa por ID
def obtener_empresa_por_id(db: Session, empresa_id: UUID) -> Optional[Empresa]:
    """Obtener una empresa por su UUID"""
    try:
        return db.query(Empresa).filter(Empresa.id == empresa_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar empresa: {str(e)}")

# Obtener empresa por NIT (para validar unicidad)
def obtener_empresa_por_nit(db: Session, nit: str) -> Optional[Empresa]:
    """Obtener una empresa por su NIT"""
    try:
        return db.query(Empresa).filter(Empresa.nit == nit.strip()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por NIT: {str(e)}")

# Obtener empresa por nombre (para validar unicidad)
def obtener_empresa_por_nombre(db: Session, nombre: str) -> Optional[Empresa]:
    """Obtener una empresa por su nombre"""
    try:
        return db.query(Empresa).filter(Empresa.nombre == nombre.upper().strip()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por nombre: {str(e)}")

# Crear nueva empresa
def crear_empresa(db: Session, empresa: EmpresaCrear) -> Empresa:
    """Crear una nueva empresa"""
    try:
        # CORREGIDO: Usar empresa.nombre (no Empresa.nombre)
        nueva_empresa = Empresa(
            nombre=empresa.nombre.upper().strip(),  # Normalizar a mayúsculas
            nit=empresa.nit.strip(),
            direccion=empresa.direccion.strip() if empresa.direccion else None,
            telefono=empresa.telefono.strip() if empresa.telefono else None,
            email=empresa.email.lower().strip() if empresa.email else None,
            sede=empresa.sede.upper().strip() if empresa.sede else None
        )
        
        db.add(nueva_empresa)
        db.commit()  # CORREGIDO: agregar paréntesis ()
        db.refresh(nueva_empresa)
        
        return nueva_empresa
        
    except IntegrityError as e:
        db.rollback()
        # Detectar si es por NIT duplicado o nombre duplicado
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            raise Exception(f"Error: Ya existe una empresa con ese NIT o nombre")
        raise Exception(f"Error de integridad al crear empresa: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear empresa: {str(e)}")

# Actualizar empresa existente
def actualizar_empresa(
    db: Session, 
    empresa_id: UUID, 
    empresa_data: EmpresaActualizar
) -> Optional[Empresa]:
    """Actualizar una empresa existente"""
    try:
        empresa = obtener_empresa_por_id(db, empresa_id)
        
        if not empresa:
            return None
        
        # Actualizar solo los campos que vienen en la petición
        if empresa_data.nombre is not None:
            empresa.nombre = empresa_data.nombre.upper().strip()
        
        if empresa_data.nit is not None:
            empresa.nit = empresa_data.nit.strip()
        
        if empresa_data.direccion is not None:
            empresa.direccion = empresa_data.direccion.strip()
        
        if empresa_data.telefono is not None:
            empresa.telefono = empresa_data.telefono.strip()
        
        if empresa_data.email is not None:
            empresa.email = empresa_data.email.lower().strip()
        
        if empresa_data.sede is not None:
            empresa.sede = empresa_data.sede.upper().strip()
        
        db.commit()
        db.refresh(empresa)
        
        return empresa
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: Ya existe una empresa con ese NIT o nombre")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar empresa: {str(e)}")

# Eliminar empresa
def eliminar_empresa(db: Session, empresa_id: UUID) -> bool:
    """Eliminar una empresa"""
    try:
        empresa = obtener_empresa_por_id(db, empresa_id)
        
        if not empresa:
            return False
        
        db.delete(empresa)
        db.commit()
        
        return True
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: No se puede eliminar la empresa porque tiene registros relacionados")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar empresa: {str(e)}")