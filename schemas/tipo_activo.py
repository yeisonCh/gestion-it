from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional


class CrearTipoActivo(BaseModel):
    nombre: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Nombre del tipo de activo",
        example="Computador", 
        title="Nombre del tipo de activo"
    )
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        # Validar que no sea solo espacios
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        
        # Eliminar espacios al inicio y final, convertir a mayúsculas
        v = v.strip().upper()
        
        # Validar que solo tenga letras, números y espacios
        if not all(c.isalnum() or c.isspace() for c in v):
            raise ValueError('El nombre solo puede contener letras, números y espacios')
        
        # Validar que no tenga múltiples espacios seguidos
        if '  ' in v:
            raise ValueError('El nombre no puede tener espacios dobles')
        
        return v

class ActualizarTipoActivo(BaseModel):
    nombre: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Nombre del tipo de activo",
        example="Computador Portátil"
    )
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        
        v = v.strip().upper()
        
        if not all(c.isalnum() or c.isspace() for c in v):
            raise ValueError('El nombre solo puede contener letras, números y espacios')
        
        if '  ' in v:
            raise ValueError('El nombre no puede tener espacios dobles')
        
        return v

class TipoActivoRespuesta(BaseModel):
    id: UUID
    nombre: str
    
    class Config:
        from_attributes = True