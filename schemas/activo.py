# app/schemas/activo.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum

# Enums para valores fijos (como en .NET)
class EstadoActivoEnum(str, Enum):
    ACTIVO = "activo"
    DANADO = "dañado"
    EN_MANTENIMIENTO = "en_mantenimiento"
    BAJA = "baja"

class ActivoCrear(BaseModel):
    serial: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Número de serie único del activo",
        example="SN-123456"
    )
    nombre: Optional[str] = Field(
        None,
        max_length=100,
        description="Nombre descriptivo del activo",
        example="Laptop Dell XPS 15"
    )
    marca: Optional[str] = Field(
        None,
        max_length=50,
        description="Marca del activo",
        example="Dell"
    )
    modelo: Optional[str] = Field(
        None,
        max_length=50,
        description="Modelo del activo",
        example="XPS 15-9520"
    )
    fecha_compra: Optional[date] = Field(
        None,
        description="Fecha de compra",
        example="2024-01-15"
    )
    estado: EstadoActivoEnum = Field(
        default=EstadoActivoEnum.ACTIVO,
        description="Estado del activo"
    )
    tipo_activo_id: UUID = Field(
        ...,
        description="ID del tipo de activo (debe existir)"
    )
    empresa_id: UUID = Field(
        ...,
        description="ID de la empresa (debe existir)"
    )
    usuario_responsable_id: Optional[UUID] = Field(
        None,
        description="ID del usuario responsable (opcional)"
    )
    
    @field_validator('serial')
    @classmethod
    def validar_serial(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El serial no puede estar vacío')
        
        v = v.strip().upper()
        
        # Solo letras, números y guiones
        if not all(c.isalnum() or c == '-' for c in v):
            raise ValueError('El serial solo puede contener letras, números y guiones')
        
        return v
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        
        if not v.strip():
            return None
        
        return v.strip().title()
    
    @field_validator('marca')
    @classmethod
    def validar_marca(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        
        if not v.strip():
            return None
        
        return v.strip().title()
    
    @field_validator('fecha_compra')
    @classmethod
    def validar_fecha_compra(cls, v: Optional[date]) -> Optional[date]:
        if v and v > date.today():
            raise ValueError('La fecha de compra no puede ser futura')
        return v


class ActivoActualizar(BaseModel):
    """Para actualizar activo (todos los campos opcionales)"""
    serial: Optional[str] = Field(None, min_length=1, max_length=100)
    nombre: Optional[str] = Field(None, max_length=100)
    marca: Optional[str] = Field(None, max_length=50)
    modelo: Optional[str] = Field(None, max_length=50)
    fecha_compra: Optional[date] = None
    estado: Optional[EstadoActivoEnum] = None
    tipo_activo_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    usuario_responsable_id: Optional[UUID] = None
    
    @field_validator('serial')
    @classmethod
    def validar_serial(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('El serial no puede estar vacío')
        return v.strip().upper()


class ActivoRespuesta(BaseModel):
    """Respuesta de activo (lo que se devuelve al cliente)"""
    id: UUID
    serial: str
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    fecha_compra: Optional[date] = None
    estado: str
    tipo_activo_id: UUID
    empresa_id: UUID
    usuario_responsable_id: Optional[UUID] = None

    class Config:
        from_attributes = True