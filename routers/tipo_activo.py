# app/routers/tipo_activo.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db
from services.tipo_activo import (
    service_obtener_tipos_activo,
    service_obtener_tipo_activo_por_id,
    service_crear_tipo_activo,
    service_actualizar_tipo_activo,
    service_eliminar_tipo_activo
)
from schemas.tipo_activo import (
    CrearTipoActivo,
    ActualizarTipoActivo,
    TipoActivoRespuesta
)


router = APIRouter(
    prefix="/api/tipos-activo",
    tags=["Tipos de Activo"]
)

# GET: api/tipos-activo
@router.get(
    "/",
    response_model=List[TipoActivoRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los tipos de activo",
    description="Retorna una lista con todos los tipos de activo registrados"
)
def obtener_tipos_activo(
    db: Session = Depends(get_db)
):
    """
    Obtener todos los tipos de activo
    
    - **No requiere parámetros**
    - Retorna una lista de tipos de activo
    """
    try:
        return service_obtener_tipos_activo(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipos de activo: {str(e)}"
        )


# GET: api/tipos-activo/{id}
@router.get(
    "/{tipo_activo_id}",
    response_model=TipoActivoRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener tipo de activo por ID",
    description="Retorna un tipo de activo específico por su UUID"
)
def obtener_tipo_activo_por_id(
    tipo_activo_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Obtener un tipo de activo por su ID
    """
    try:
        resultado = service_obtener_tipo_activo_por_id(db, tipo_activo_id)
        
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de activo con ID {tipo_activo_id} no encontrado"
            )
        
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipo de activo: {str(e)}"
        )


# POST: api/tipos-activo
@router.post(
    "/",
    response_model=TipoActivoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo tipo de activo",
    description="Crea un nuevo tipo de activo con validaciones"
)
def crear_tipo_activo(
    tipo_activo: CrearTipoActivo,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo tipo de activo
    
    - **nombre**: Nombre del tipo de activo (mínimo 3, máximo 50 caracteres)
    - El nombre se guarda en mayúsculas automáticamente
    - No se permiten nombres duplicados
    """
    try:
        return service_crear_tipo_activo(db, tipo_activo)
    except Exception as e:
        # Capturar error de duplicado
        if "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear tipo de activo: {str(e)}"
        )


# PUT: api/tipos-activo/{id}
@router.put(
    "/{tipo_activo_id}",
    response_model=TipoActivoRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar tipo de activo",
    description="Actualiza un tipo de activo existente"
)
def actualizar_tipo_activo(
    tipo_activo_id: UUID,
    tipo_activo: ActualizarTipoActivo,
    db: Session = Depends(get_db)
):
    """
    Actualizar un tipo de activo existente
    
    - **tipo_activo_id**: UUID del tipo de activo a actualizar
    - **nombre**: (opcional) Nuevo nombre del tipo de activo
    """
    try:
        resultado = service_actualizar_tipo_activo(db, tipo_activo_id, tipo_activo)
        
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de activo con ID {tipo_activo_id} no encontrado"
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
            detail=f"Error al actualizar tipo de activo: {str(e)}"
        )


# DELETE: api/tipos-activo/{id}
@router.delete(
    "/{tipo_activo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tipo de activo",
    description="Elimina un tipo de activo (solo si no tiene activos relacionados)"
)
def eliminar_tipo_activo(
    tipo_activo_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Eliminar un tipo de activo
    
    - **tipo_activo_id**: UUID del tipo de activo a eliminar
    - Solo se puede eliminar si no tiene activos asociados
    """
    try:
        resultado = service_eliminar_tipo_activo(db, tipo_activo_id)
        
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de activo con ID {tipo_activo_id} no encontrado"
            )
        
        return None  # 204 No Content no retorna cuerpo
    except HTTPException:
        raise
    except Exception as e:
        if "tiene registros relacionados" in str(e) or "activos relacionados" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el tipo de activo porque tiene activos asociados"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar tipo de activo: {str(e)}"
        )

