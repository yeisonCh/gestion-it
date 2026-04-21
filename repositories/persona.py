from sqlalchemy.orm import Session
from models.persona import Persona
from schemas.persona import PersonaCrear

def obtener_personas(db: Session):
    return db.query(Persona).all()

def obtener_persona_por_id(db: Session, persona_id: int):
    return db.query(Persona).filter(Persona.id == persona_id).first()

def crear_persona(db: Session, persona: PersonaCrear):
    nueva_persona = Persona(
        nombres=persona.nombres,
        apellidos=persona.apellidos,
        tipo_documento=persona.tipo_documento,
        numero_documento=persona.numero_documento,
        telefono=persona.telefono,
        email=persona.email
    )
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona)
    return nueva_persona