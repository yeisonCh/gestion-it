from pydantic import BaseModel
from uuid import UUID


class CrearTipoActivo(BaseModel):
    nombre: str

class TipoActivoRespuesta(BaseModel):
    id: UUID
    nombre: str
    
    class Config:
        from_attributes = True