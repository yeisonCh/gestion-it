from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.tipo_activo import TipoActivoRespuesta, CrearTipoActivo

