# app/schemas/tecnico.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from uuid import UUID

class TecnicoCrear(BaseModel):
    especialidad: Optional[str] = Field(None, max_length=100, description="Especialidad del técnico")
    tipo: str = Field(..., description="Tipo: interno o externo")
    persona_id: UUID = Field(..., description="ID de la persona asociada")
    empresas_ids: Optional[List[UUID]] = Field(None, description="Lista de empresas a las que pertenece")

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ['interno', 'externo']:
            raise ValueError('El tipo debe ser "interno" o "externo"')
        return v

class TecnicoActualizar(BaseModel):
    especialidad: Optional[str] = Field(None, max_length=100)
    tipo: Optional[str] = None
    persona_id: Optional[UUID] = None
    empresas_ids: Optional[List[UUID]] = None

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: Optional[str]) -> Optional[str]:
        if v:
            v = v.lower().strip()
            if v not in ['interno', 'externo']:
                raise ValueError('El tipo debe ser "interno" o "externo"')
        return v

class TecnicoRespuesta(BaseModel):
    id: UUID
    especialidad: Optional[str] = None
    tipo: str
    persona_id: UUID
    nombre_persona: Optional[str] = None  # Campo adicional para mostrar el nombre

    class Config:
        from_attributes = True