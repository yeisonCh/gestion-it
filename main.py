from fastapi import FastAPI
from database import crear_base_de_datos_si_no_existe, engine, Base
import models

app = FastAPI()

@app.on_event("startup")
async def startup():
    crear_base_de_datos_si_no_existe()
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}