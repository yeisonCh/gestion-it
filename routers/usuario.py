# app/routers/usuario.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from database import get_db
from schemas.usuario import (
    UsuarioCrear, 
    UsuarioActualizar, 
    UsuarioRespuesta, 
    UsuarioLogin
)
from services.usuario import (
    service_obtener_usuarios,
    service_obtener_usuario_por_id,
    service_obtener_usuario_por_username,
    service_obtener_usuarios_por_empresa,
    service_obtener_usuarios_por_rol,
    service_obtener_usuarios_habilitados,
    service_crear_usuario,
    service_actualizar_usuario,
    service_eliminar_usuario,
    service_borrar_usuario_permanentemente,
    service_autenticar_usuario
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


# GET: /usuarios
@router.get(
    "/", 
    response_model=List[UsuarioRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los usuarios",
    description="Retorna una lista con todos los usuarios registrados"
)
def listar_usuarios(db: Session = Depends(get_db)):
    try:
        return service_obtener_usuarios(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}"
        )


# GET: /usuarios/{usuario_id}
@router.get(
    "/{usuario_id}", 
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico por su UUID"
)
def obtener_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        usuario = service_obtener_usuario_por_id(db, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}"
        )


# GET: /usuarios/buscar/username?username={username}
@router.get(
    "/buscar/username",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Buscar usuario por username",
    description="Retorna un usuario por su nombre de usuario"
)
def buscar_usuario_por_username(
    username: str = Query(..., description="Nombre de usuario", example="jperez"),
    db: Session = Depends(get_db)
):
    try:
        usuario = service_obtener_usuario_por_username(db, username)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con username '{username}' no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar usuario: {str(e)}"
        )


# GET: /usuarios/filtros/empresa?empresa_id={id}
@router.get(
    "/filtros/empresa",
    response_model=List[UsuarioRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener usuarios por empresa",
    description="Retorna todos los usuarios de una empresa específica"
)
def obtener_usuarios_por_empresa(
    empresa_id: UUID = Query(..., description="ID de la empresa"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_usuarios_por_empresa(db, empresa_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios por empresa: {str(e)}"
        )


# GET: /usuarios/filtros/rol?rol={rol}
@router.get(
    "/filtros/rol",
    response_model=List[UsuarioRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener usuarios por rol",
    description="Retorna todos los usuarios con un rol específico (admin/operativo)"
)
def obtener_usuarios_por_rol(
    rol: str = Query(..., description="Rol del usuario", example="operativo"),
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_usuarios_por_rol(db, rol)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios por rol: {str(e)}"
        )


# GET: /usuarios/filtros/habilitados
@router.get(
    "/filtros/habilitados",
    response_model=List[UsuarioRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener usuarios habilitados",
    description="Retorna solo los usuarios habilitados"
)
def obtener_usuarios_habilitados(
    db: Session = Depends(get_db)
):
    try:
        return service_obtener_usuarios_habilitados(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios habilitados: {str(e)}"
        )


# POST: /usuarios/login (autenticación)
@router.post(
    "/login",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Autenticar usuario",
    description="Autentica un usuario por username y password"
)
def login(
    login_data: UsuarioLogin,
    db: Session = Depends(get_db)
):
    try:
        return service_autenticar_usuario(db, login_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# POST: /usuarios
@router.post(
    "/", 
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario",
    description="Crea un nuevo usuario con validaciones (username único, persona existente, empresa existente)"
)
def crear_usuario(
    usuario: UsuarioCrear, 
    db: Session = Depends(get_db)
):
    try:
        return service_crear_usuario(db, usuario)
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
            detail=f"Error al crear usuario: {str(e)}"
        )


# PUT: /usuarios/{usuario_id}
@router.put(
    "/{usuario_id}",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario",
    description="Actualiza un usuario existente"
)
def actualizar_usuario(
    usuario_id: UUID,
    usuario_data: UsuarioActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_actualizar_usuario(db, usuario_id, usuario_data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
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
            detail=f"Error al actualizar usuario: {str(e)}"
        )


# DELETE: /usuarios/{usuario_id} (borrado lógico)
@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario (borrado lógico)",
    description="Deshabilita un usuario en lugar de eliminarlo físicamente"
)
def eliminar_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_eliminar_usuario(db, usuario_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        return {"mensaje": f"Usuario {usuario_id} deshabilitado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}"
        )


# DELETE: /usuarios/{usuario_id}/permanente (borrado físico)
@router.delete(
    "/{usuario_id}/permanente",
    status_code=status.HTTP_200_OK,
    summary="Borrar usuario permanentemente",
    description="Elimina físicamente un usuario de la base de datos (con precaución)"
)
def borrar_usuario_permanentemente(
    usuario_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_borrar_usuario_permanentemente(db, usuario_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        return {"mensaje": f"Usuario {usuario_id} eliminado permanentemente"}
    except HTTPException:
        raise
    except Exception as e:
        if "registros relacionados" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el usuario porque tiene registros relacionados"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al borrar usuario: {str(e)}"
        )