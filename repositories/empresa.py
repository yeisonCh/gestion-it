from sqlalchemy.orm import Session
from models.empresa import Empresa
from schemas.empresa import EmpresaCrear

def obtener_empresas(db: Session):
    return db.query(Empresa).all()

def obtener_empresa_por_id(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def crear_empresa(db: Session, empresa: EmpresaCrear):
    nueva_empresa = Empresa(
        nombre=empresa.nombre,
        nit=empresa.nit,
        direccion=empresa.direccion,
        telefono=empresa.telefono,
        email=empresa.email,
        sede=empresa.sede
    )
    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)
    return nueva_empresa