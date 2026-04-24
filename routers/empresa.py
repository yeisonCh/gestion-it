# app/routers/empresa.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db
from schemas.empresa import EmpresaCrear, EmpresaActualizar, EmpresaRespuesta
from services.empresa import (
    service_obtener_empresas,
    service_obtener_empresa_por_id,
    service_crear_empresa,
    service_actualizar_empresa,
    service_eliminar_empresa
)

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)

# GET: /empresas
@router.get(
    "/", 
    response_model=List[EmpresaRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todas las empresas",
    description="Retorna una lista con todas las empresas registradas"
)
def listar_empresas(db: Session = Depends(get_db)):
    try:
        return service_obtener_empresas(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empresas: {str(e)}"
        )

# GET: /empresas/{empresa_id}
@router.get(
    "/{empresa_id}", 
    response_model=EmpresaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener empresa por ID",
    description="Retorna una empresa específica por su UUID"
)
def obtener_empresa(
    empresa_id: UUID,  # CORREGIDO: int -> UUID
    db: Session = Depends(get_db)
):
    try:
        empresa = service_obtener_empresa_por_id(db, empresa_id)
        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa con ID {empresa_id} no encontrada"
            )
        return empresa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empresa: {str(e)}"
        )

# POST: /empresas
@router.post(
    "/", 
    response_model=EmpresaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva empresa",
    description="Crea una nueva empresa con validaciones de NIT y nombre únicos"
)
def crear_empresa(
    empresa: EmpresaCrear, 
    db: Session = Depends(get_db)
):
    try:
        return service_crear_empresa(db, empresa)
    except Exception as e:
        # Capturar errores de duplicado (NIT o nombre ya existen)
        if "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear empresa: {str(e)}"
        )

# PUT: /empresas/{empresa_id}
@router.put(
    "/{empresa_id}",
    response_model=EmpresaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar empresa",
    description="Actualiza una empresa existente"
)
def actualizar_empresa(
    empresa_id: UUID,
    empresa_data: EmpresaActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_actualizar_empresa(db, empresa_id, empresa_data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa con ID {empresa_id} no encontrada"
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar empresa: {str(e)}"
        )

# DELETE: /empresas/{empresa_id}
@router.delete(
    "/{empresa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar empresa",
    description="Elimina una empresa (solo si no tiene activos relacionados)"
)
def eliminar_empresa(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_eliminar_empresa(db, empresa_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa con ID {empresa_id} no encontrada"
            )
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        if "registros relacionados" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar la empresa porque tiene activos o ubicaciones asociadas"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar empresa: {str(e)}"
        )