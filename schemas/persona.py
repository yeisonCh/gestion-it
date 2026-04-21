from pydantic import BaseModel
from typing import Optional

class PersonaCrear(BaseModel):
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    telefono: Optional[str] = None
    email: Optional[str] = None

class PersonaRespuesta(BaseModel):
    id: int
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    telefono: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True