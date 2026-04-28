# app/routers/activo_relacion.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from database import get_db
from schemas.activo_relacion import (
    ActivoRelacionCrear,
    ActivoRelacionActualizar,
    ActivoRelacionRespuesta
)
from services.activo_relacion import (
    service_obtener_relaciones,
    service_obtener_relacion_por_id,
    service_obtener_relaciones_por_padre,
    service_obtener_relaciones_por_hijo,
    service_obtener_relaciones_activas,
    service_crear_relacion,
    service_finalizar_relacion
)

router = APIRouter(
    prefix="/activos-relaciones",
    tags=["Activos Relaciones"]
)


# GET: /activos-relaciones
@router.get(
    "/",
    response_model=List[ActivoRelacionRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todas las relaciones",
    description="Retorna una lista con todas las relaciones entre activos"
)
def listar_relaciones(db: Session = Depends(get_db)):
    try:
        return service_obtener_relaciones(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener relaciones: {str(e)}"
        )


# GET: /activos-relaciones/activas
@router.get(
    "/activas",
    response_model=List[ActivoRelacionRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener relaciones activas",
    description="Retorna solo las relaciones activas (sin fecha_fin)"
)
def listar_relaciones_activas(db: Session = Depends(get_db)):
    try:
        return service_obtener_relaciones_activas(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener relaciones activas: {str(e)}"
        )


# GET: /activos-relaciones/{relacion_id}
@router.get(
    "/{relacion_id}",
    response_model=ActivoRelacionRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener relación por ID",
    description="Retorna una relación específica por su UUID"
)
def obtener_relacion(
    relacion_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        relacion = service_obtener_relacion_por_id(db, relacion_id)
        if not relacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Relación con ID {relacion_id} no encontrada"
            )
        return relacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener relación: {str(e)}"
        )


# GET: /activos-relaciones/padre/{activo_padre_id}
@router.get(
    "/padre/{activo_padre_id}",
    response_model=List[ActivoRelacionRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener relaciones por activo padre",
    description="Retorna todas las relaciones donde el activo es padre"
)
def obtener_relaciones_por_padre(
    activo_padre_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_relaciones_por_padre(db, activo_padre_id)
    except Exception as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener relaciones: {str(e)}"
        )


# GET: /activos-relaciones/hijo/{activo_hijo_id}
@router.get(
    "/hijo/{activo_hijo_id}",
    response_model=List[ActivoRelacionRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener relaciones por activo hijo",
    description="Retorna todas las relaciones donde el activo es hijo"
)
def obtener_relaciones_por_hijo(
    activo_hijo_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_relaciones_por_hijo(db, activo_hijo_id)
    except Exception as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener relaciones: {str(e)}"
        )


# POST: /activos-relaciones
@router.post(
    "/",
    response_model=ActivoRelacionRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva relación",
    description="Crea una nueva relación entre un activo padre y un activo hijo"
)
def crear_relacion(
    relacion: ActivoRelacionCrear,
    db: Session = Depends(get_db)
):
    try:
        return service_crear_relacion(db, relacion)
    except Exception as e:
        if "no existe" in str(e) or "Ya existe" in str(e) or "No se puede" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear relación: {str(e)}"
        )


# PUT: /activos-relaciones/{relacion_id}/finalizar
@router.put(
    "/{relacion_id}/finalizar",
    response_model=ActivoRelacionRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Finalizar relación",
    description="Finaliza una relación activa (agrega fecha_fin y motivo)"
)
def finalizar_relacion(
    relacion_id: UUID,
    data: ActivoRelacionActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_finalizar_relacion(db, relacion_id, data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Relación con ID {relacion_id} no encontrada"
            )
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        if "ya está finalizada" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al finalizar relación: {str(e)}"
        )