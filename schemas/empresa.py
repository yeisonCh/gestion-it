from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class EmpresaCrear(BaseModel):
    nombre: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sede: Optional[str] = None

class EmpresaRespuesta(BaseModel):
    id: UUID
    nombre: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sede: Optional[str] = None

    class Config:
        from_attributes = True