# app/services/usuario.py

from sqlalchemy.orm import Session
from repositories.usuario import (
    obtener_usuarios,
    obtener_usuario_por_id,
    obtener_usuario_por_username,
    obtener_usuarios_por_empresa,
    obtener_usuarios_por_rol,
    obtener_usuarios_habilitados,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    borrar_usuario_permanentemente
)
from repositories.persona import obtener_persona_por_id
from repositories.empresa import obtener_empresa_por_id
from schemas.usuario import UsuarioCrear, UsuarioActualizar, UsuarioLogin
from uuid import UUID
from typing import List, Optional

# Obtener todos los usuarios
def service_obtener_usuarios(db: Session):
    """Obtener todos los usuarios"""
    return obtener_usuarios(db)

# Obtener usuario por ID
def service_obtener_usuario_por_id(db: Session, usuario_id: UUID):
    """Obtener un usuario por su ID"""
    return obtener_usuario_por_id(db, usuario_id)

# Obtener usuario por username
def service_obtener_usuario_por_username(db: Session, username: str):
    """Obtener un usuario por su username"""
    return obtener_usuario_por_username(db, username)

# Obtener usuarios por empresa
def service_obtener_usuarios_por_empresa(db: Session, empresa_id: UUID):
    """Obtener usuarios filtrados por empresa"""
    return obtener_usuarios_por_empresa(db, empresa_id)

# Obtener usuarios por rol
def service_obtener_usuarios_por_rol(db: Session, rol: str):
    """Obtener usuarios filtrados por rol"""
    return obtener_usuarios_por_rol(db, rol)

# Obtener usuarios habilitados
def service_obtener_usuarios_habilitados(db: Session):
    """Obtener solo usuarios habilitados"""
    return obtener_usuarios_habilitados(db)

# Crear nuevo usuario (con validaciones de negocio)
def service_crear_usuario(db: Session, usuario: UsuarioCrear):
    """
    Crear un nuevo usuario
    - Valida que el username no exista
    - Valida que la persona exista
    - Valida que la empresa exista
    """
    # Validación 1: ¿Ya existe un usuario con ese username?
    existe_username = obtener_usuario_por_username(db, usuario.username)
    if existe_username:
        raise Exception(f"Ya existe un usuario con el username '{usuario.username}'")
    
    # Validación 2: ¿Existe la persona?
    persona = obtener_persona_por_id(db, usuario.persona_id)
    if not persona:
        raise Exception(f"La persona con ID {usuario.persona_id} no existe")
    
    # Validación 3: ¿Existe la empresa?
    empresa = obtener_empresa_por_id(db, usuario.empresa_id)
    if not empresa:
        raise Exception(f"La empresa con ID {usuario.empresa_id} no existe")
    
    # TODO: Hash de contraseña (lo haremos después)
    
    return crear_usuario(db, usuario)

# Actualizar usuario existente
def service_actualizar_usuario(
    db: Session, 
    usuario_id: UUID, 
    usuario_data: UsuarioActualizar
):
    """
    Actualizar un usuario existente
    - Valida que el usuario existe
    - Valida que el nuevo username no pertenezca a otro usuario
    - Valida que la persona exista (si se actualiza)
    - Valida que la empresa exista (si se actualiza)
    """
    # Validación 1: ¿Existe el usuario?
    existe = obtener_usuario_por_id(db, usuario_id)
    if not existe:
        raise Exception(f"Usuario con ID {usuario_id} no encontrado")
    
    # Validación 2: Si está actualizando el username, ¿el nuevo username ya existe en otro usuario?
    if usuario_data.username:
        username_existe = obtener_usuario_por_username(db, usuario_data.username)
        if username_existe and username_existe.id != usuario_id:
            raise Exception(f"Ya existe otro usuario con el username '{usuario_data.username}'")
    
    # Validación 3: Si está actualizando persona_id, ¿existe?
    if usuario_data.persona_id:
        persona = obtener_persona_por_id(db, usuario_data.persona_id)
        if not persona:
            raise Exception(f"La persona con ID {usuario_data.persona_id} no existe")
    
    # Validación 4: Si está actualizando empresa_id, ¿existe?
    if usuario_data.empresa_id:
        empresa = obtener_empresa_por_id(db, usuario_data.empresa_id)
        if not empresa:
            raise Exception(f"La empresa con ID {usuario_data.empresa_id} no existe")
    
    return actualizar_usuario(db, usuario_id, usuario_data)

# Eliminar usuario (borrado lógico)
def service_eliminar_usuario(db: Session, usuario_id: UUID):
    """
    Eliminar un usuario (borrado lógico - solo deshabilita)
    - Valida que el usuario existe
    """
    # Validación: ¿Existe el usuario?
    existe = obtener_usuario_por_id(db, usuario_id)
    if not existe:
        raise Exception(f"Usuario con ID {usuario_id} no encontrado")
    
    return eliminar_usuario(db, usuario_id)

# Borrar usuario permanentemente (con cuidado)
def service_borrar_usuario_permanentemente(db: Session, usuario_id: UUID):
    """
    Borrar usuario permanentemente (con precaución)
    - Valida que el usuario existe
    """
    # Validación: ¿Existe el usuario?
    existe = obtener_usuario_por_id(db, usuario_id)
    if not existe:
        raise Exception(f"Usuario con ID {usuario_id} no encontrado")
    
    return borrar_usuario_permanentemente(db, usuario_id)

# Autenticación de usuario (para login)
def service_autenticar_usuario(db: Session, login_data: UsuarioLogin):
    """
    Autenticar un usuario por username y password
    - Valida que el usuario existe
    - Valida que la contraseña sea correcta
    - Valida que el usuario esté habilitado
    """
    usuario = obtener_usuario_por_username(db, login_data.username)
    
    if not usuario:
        raise Exception("Usuario o contraseña incorrectos")
    
    if not usuario.habilitado:
        raise Exception("Usuario deshabilitado. Contacte al administrador")
    
    # TODO: Verificar hash de contraseña (lo haremos después)
    if usuario.password != login_data.password:
        raise Exception("Usuario o contraseña incorrectos")
    
    return usuario