from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.persona import PersonaCrear, PersonaRespuesta
from services.persona import service_obtener_personas, service_obtener_persona_por_id, service_crear_persona

router = APIRouter(
    prefix="/personas",
    tags=["Personas"]
)

@router.get("/", response_model=list[PersonaRespuesta])
def listar_personas(db: Session = Depends(get_db)):
    return service_obtener_personas(db)

@router.get("/{persona_id}", response_model=PersonaRespuesta)
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = service_obtener_persona_por_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.post("/", response_model=PersonaRespuesta)
def crear_persona(persona: PersonaCrear, db: Session = Depends(get_db)):
    return service_crear_persona(db, persona)