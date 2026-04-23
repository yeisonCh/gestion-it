from sqlalchemy.orm import Session
from repositories.persona import obtener_personas, obtener_persona_por_id, crear_persona
from schemas.persona import PersonaCrear
from uuid import UUID

def service_obtener_personas(db: Session):
    return obtener_personas(db)

def service_obtener_persona_por_id(db: Session, persona_id: UUID):
    return obtener_persona_por_id(db, persona_id)

def service_crear_persona(db: Session, persona: PersonaCrear):
    return crear_persona(db, persona)