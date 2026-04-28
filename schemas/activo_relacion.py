# app/schemas/activo_relacion.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import date

class ActivoRelacionCrear(BaseModel):
    activo_padre_id: UUID = Field(..., description="ID del activo padre")
    activo_hijo_id: UUID = Field(..., description="ID del activo hijo")
    fecha_asignacion: date = Field(..., description="Fecha de asignación")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin (opcional)")
    motivo_retiro: Optional[str] = Field(None, max_length=200, description="Motivo de retiro")

    @field_validator('fecha_asignacion')
    @classmethod
    def validar_fecha_asignacion(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('La fecha de asignación no puede ser futura')
        return v

    @field_validator('fecha_fin')
    @classmethod
    def validar_fecha_fin(cls, v: Optional[date], info) -> Optional[date]:
        if v and info.data.get('fecha_asignacion') and v < info.data['fecha_asignacion']:
            raise ValueError('La fecha de fin no puede ser anterior a la fecha de asignación')
        return v

class ActivoRelacionActualizar(BaseModel):
    fecha_fin: Optional[date] = None
    motivo_retiro: Optional[str] = Field(None, max_length=200)

class ActivoRelacionRespuesta(BaseModel):
    id: UUID
    activo_padre_id: UUID
    activo_hijo_id: UUID
    fecha_asignacion: date
    fecha_fin: Optional[date] = None
    motivo_retiro: Optional[str] = None

    class Config:
        from_attributes = True