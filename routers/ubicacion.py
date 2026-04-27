# app/routers/ubicacion.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db
from schemas.ubicacion import UbicacionCrear, UbicacionActualizar, UbicacionRespuesta
from services.ubicacion import (
    service_obtener_ubicaciones,
    service_obtener_ubicacion_por_id,
    service_obtener_ubicaciones_por_empresa,
    service_crear_ubicacion,
    service_actualizar_ubicacion
)

router = APIRouter(
    prefix="/ubicaciones",
    tags=["Ubicaciones"]
)


# GET: /ubicaciones
@router.get(
    "/",
    response_model=List[UbicacionRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todas las ubicaciones",
    description="Retorna una lista con todas las ubicaciones registradas"
)
def listar_ubicaciones(db: Session = Depends(get_db)):
    try:
        return service_obtener_ubicaciones(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones: {str(e)}"
        )


# GET: /ubicaciones/{ubicacion_id}
@router.get(
    "/{ubicacion_id}",
    response_model=UbicacionRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener ubicación por ID",
    description="Retorna una ubicación específica por su UUID"
)
def obtener_ubicacion(
    ubicacion_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        ubicacion = service_obtener_ubicacion_por_id(db, ubicacion_id)
        if not ubicacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {ubicacion_id} no encontrada"
            )
        return ubicacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicación: {str(e)}"
        )


# GET: /ubicaciones/empresa/{empresa_id}
@router.get(
    "/empresa/{empresa_id}",
    response_model=List[UbicacionRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener ubicaciones por empresa",
    description="Retorna todas las ubicaciones de una empresa específica"
)
def listar_ubicaciones_por_empresa(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_ubicaciones_por_empresa(db, empresa_id)
    except Exception as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones: {str(e)}"
        )


# POST: /ubicaciones
@router.post(
    "/",
    response_model=UbicacionRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva ubicación",
    description="Crea una nueva ubicación"
)
def crear_ubicacion(
    ubicacion: UbicacionCrear,
    db: Session = Depends(get_db)
):
    try:
        return service_crear_ubicacion(db, ubicacion)
    except Exception as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear ubicación: {str(e)}"
        )


# PUT: /ubicaciones/{ubicacion_id}
@router.put(
    "/{ubicacion_id}",
    response_model=UbicacionRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar ubicación",
    description="Actualiza una ubicación existente"
)
def actualizar_ubicacion(
    ubicacion_id: UUID,
    ubicacion_data: UbicacionActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_actualizar_ubicacion(db, ubicacion_id, ubicacion_data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {ubicacion_id} no encontrada"
            )
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar ubicación: {str(e)}"
        )