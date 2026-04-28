from fastapi import FastAPI
from database import crear_base_de_datos_si_no_existe, engine, Base
from routers import (
    empresa_router, 
    persona_router, 
    tipo_activo_router, 
    usuario_router, 
    ubicacion_router, 
    activo_router, 
    tecnico_router)

app = FastAPI()

@app.on_event("startup")
async def startup():
    crear_base_de_datos_si_no_existe()
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas verificadas/creadas.")

app.include_router(activo_router)
app.include_router(empresa_router)
app.include_router(persona_router)
app.include_router(tipo_activo_router)
app.include_router(tecnico_router)
app.include_router(usuario_router)
app.include_router(ubicacion_router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}