# app/routers/activo.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from database import get_db
from schemas.activo import ActivoCrear, ActivoActualizar, ActivoRespuesta
from services.activo import (
    service_obtener_activos,
    service_obtener_activo_por_id,
    service_obtener_activos_por_tipo,
    service_obtener_activos_por_empresa,
    service_obtener_activos_por_estado,
    service_crear_activo,
    service_actualizar_activo,
    service_eliminar_activo
)

router = APIRouter(
    prefix="/activos",
    tags=["Activos"]
)

# GET: /activos
@router.get(
    "/", 
    response_model=List[ActivoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los activos",
    description="Retorna una lista con todos los activos registrados"
)
def listar_activos(db: Session = Depends(get_db)):
    try:
        return service_obtener_activos(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener activos: {str(e)}"
        )

# GET: /activos/{activo_id}
@router.get(
    "/{activo_id}", 
    response_model=ActivoRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener activo por ID",
    description="Retorna un activo específico por su UUID"
)
def obtener_activo(
    activo_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        activo = service_obtener_activo_por_id(db, activo_id)
        if not activo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Activo con ID {activo_id} no encontrado"
            )
        return activo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener activo: {str(e)}"
        )

# GET: /activos/filtros/tipo?tipo_activo_id={id}
@router.get(
    "/filtros/tipo",
    response_model=List[ActivoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener activos por tipo",
    description="Retorna todos los activos de un tipo específico"
)
def obtener_activos_por_tipo(
    tipo_activo_id: UUID = Query(..., description="ID del tipo de activo"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_activos_por_tipo(db, tipo_activo_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener activos por tipo: {str(e)}"
        )

# GET: /activos/filtros/empresa?empresa_id={id}
@router.get(
    "/filtros/empresa",
    response_model=List[ActivoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener activos por empresa",
    description="Retorna todos los activos de una empresa específica"
)
def obtener_activos_por_empresa(
    empresa_id: UUID = Query(..., description="ID de la empresa"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_activos_por_empresa(db, empresa_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener activos por empresa: {str(e)}"
        )

# GET: /activos/filtros/estado?estado={estado}
@router.get(
    "/filtros/estado",
    response_model=List[ActivoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener activos por estado",
    description="Retorna todos los activos con un estado específico (activo, dañado, en_mantenimiento, baja)"
)
def obtener_activos_por_estado(
    estado: str = Query(..., description="Estado del activo", example="activo"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_activos_por_estado(db, estado)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener activos por estado: {str(e)}"
        )

# POST: /activos
@router.post(
    "/", 
    response_model=ActivoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo activo",
    description="Crea un nuevo activo con validaciones (serial único, tipo_activo existente, empresa existente)"
)
def crear_activo(
    activo: ActivoCrear, 
    db: Session = Depends(get_db)
):
    try:
        return service_crear_activo(db, activo)
    except Exception as e:
        if "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear activo: {str(e)}"
        )

# PUT: /activos/{activo_id}
@router.put(
    "/{activo_id}",
    response_model=ActivoRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar activo",
    description="Actualiza un activo existente"
)
def actualizar_activo(
    activo_id: UUID,
    activo_data: ActivoActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_actualizar_activo(db, activo_id, activo_data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Activo con ID {activo_id} no encontrado"
            )
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        if "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar activo: {str(e)}"
        )

# DELETE: /activos/{activo_id}
@router.delete(
    "/{activo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar activo",
    description="Elimina un activo (solo si no tiene registros relacionados)"
)
def eliminar_activo(
    activo_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_eliminar_activo(db, activo_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Activo con ID {activo_id} no encontrado"
            )
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        if "registros relacionados" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el activo porque tiene registros relacionados"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar activo: {str(e)}"
        )