# app/routers/tecnico.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db
from schemas.tecnico import TecnicoCrear, TecnicoActualizar, TecnicoRespuesta
from services.tecnico import (
    service_obtener_tecnico_por_id,
    service_obtener_tecnicos_por_tipo,
    service_obtener_tecnicos_por_empresa,
    service_crear_tecnico,
    service_actualizar_tecnico
)

router = APIRouter(
    prefix="/tecnicos",
    tags=["Técnicos"]
)


# GET: /tecnicos/{tecnico_id}
@router.get(
    "/{tecnico_id}",
    response_model=TecnicoRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener técnico por ID",
    description="Retorna un técnico específico por su UUID"
)
def obtener_tecnico(
    tecnico_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        tecnico = service_obtener_tecnico_por_id(db, tecnico_id)
        if not tecnico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Técnico con ID {tecnico_id} no encontrado"
            )
        return tecnico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener técnico: {str(e)}"
        )


# GET: /tecnicos/filtros/tipo?tipo={tipo}
@router.get(
    "/filtros/tipo",
    response_model=List[TecnicoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener técnicos por tipo",
    description="Retorna técnicos filtrados por tipo (interno/externo)"
)
def obtener_tecnicos_por_tipo(
    tipo: str = Query(..., description="Tipo: interno o externo"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_tecnicos_por_tipo(db, tipo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener técnicos: {str(e)}"
        )


# GET: /tecnicos/filtros/empresa?empresa_id={empresa_id}
@router.get(
    "/filtros/empresa",
    response_model=List[TecnicoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener técnicos por empresa",
    description="Retorna todos los técnicos que pertenecen a una empresa"
)
def obtener_tecnicos_por_empresa(
    empresa_id: UUID = Query(..., description="ID de la empresa"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_tecnicos_por_empresa(db, empresa_id)
    except Exception as e:
        if "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener técnicos: {str(e)}"
        )


# POST: /tecnicos
@router.post(
    "/",
    response_model=TecnicoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo técnico",
    description="Crea un nuevo técnico asociado a una persona y opcionalmente a empresas"
)
def crear_tecnico(
    tecnico: TecnicoCrear,
    db: Session = Depends(get_db)
):
    try:
        return service_crear_tecnico(db, tecnico)
    except Exception as e:
        if "ya existe" in str(e) or "no existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear técnico: {str(e)}"
        )


# PUT: /tecnicos/{tecnico_id}
@router.put(
    "/{tecnico_id}",
    response_model=TecnicoRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar técnico",
    description="Actualiza un técnico existente"
)
def actualizar_tecnico(
    tecnico_id: UUID,
    tecnico_data: TecnicoActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_actualizar_tecnico(db, tecnico_id, tecnico_data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Técnico con ID {tecnico_id} no encontrado"
            )
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        if "no existe" in str(e) or "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar técnico: {str(e)}"
        )