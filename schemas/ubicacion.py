# app/schemas/ubicacion.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID

class UbicacionCrear(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre de la ubicación")
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripción opcional")
    empresa_id: Optional[UUID] = Field(None, description="ID de la empresa")
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().upper()

class UbicacionActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=200)
    empresa_id: Optional[UUID] = None

class UbicacionRespuesta(BaseModel):
    id: UUID
    nombre: str
    descripcion: Optional[str] = None
    empresa_id: Optional[UUID] = None
    
    class Config:
        from_attributes = True