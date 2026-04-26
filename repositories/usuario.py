# app/repositories/usuario.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.usuario import Usuario
from schemas.usuario import UsuarioCrear, UsuarioActualizar
from uuid import UUID
from typing import List, Optional

# Obtener todos los usuarios
def obtener_usuarios(db: Session) -> List[Usuario]:
    """Obtener todos los usuarios ordenados por username"""
    try:
        return db.query(Usuario).order_by(Usuario.username).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener usuarios: {str(e)}")

# Obtener usuario por ID
def obtener_usuario_por_id(db: Session, usuario_id: UUID) -> Optional[Usuario]:
    """Obtener un usuario por su UUID"""
    try:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar usuario: {str(e)}")

# Obtener usuario por username (para validar unicidad y login)
def obtener_usuario_por_username(db: Session, username: str) -> Optional[Usuario]:
    """Obtener un usuario por su username"""
    try:
        return db.query(Usuario).filter(Usuario.username == username.lower().strip()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por username: {str(e)}")

# Obtener usuarios por empresa
def obtener_usuarios_por_empresa(db: Session, empresa_id: UUID) -> List[Usuario]:
    """Obtener todos los usuarios de una empresa específica"""
    try:
        return db.query(Usuario).filter(Usuario.empresa_id == empresa_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar usuarios por empresa: {str(e)}")

# Obtener usuarios por rol
def obtener_usuarios_por_rol(db: Session, rol: str) -> List[Usuario]:
    """Obtener todos los usuarios con un rol específico"""
    try:
        return db.query(Usuario).filter(Usuario.rol == rol.lower()).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar usuarios por rol: {str(e)}")

# Obtener usuarios habilitados
def obtener_usuarios_habilitados(db: Session) -> List[Usuario]:
    """Obtener todos los usuarios habilitados"""
    try:
        return db.query(Usuario).filter(Usuario.habilitado == True).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar usuarios habilitados: {str(e)}")

# Crear nuevo usuario
def crear_usuario(db: Session, usuario: UsuarioCrear) -> Usuario:
    """Crear un nuevo usuario"""
    try:
        nuevo_usuario = Usuario(
            username=usuario.username.lower().strip(),
            password=usuario.password,  # Más adelante: hashear contraseña
            rol=usuario.rol.lower().strip(),
            habilitado=usuario.habilitado,
            persona_id=usuario.persona_id,
            empresa_id=usuario.empresa_id
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        return nuevo_usuario
        
    except IntegrityError as e:
        db.rollback()
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            raise Exception(f"Error: Ya existe un usuario con el username '{usuario.username}'")
        raise Exception(f"Error de integridad al crear usuario: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear usuario: {str(e)}")

# Actualizar usuario existente
def actualizar_usuario(
    db: Session, 
    usuario_id: UUID, 
    usuario_data: UsuarioActualizar
) -> Optional[Usuario]:
    """Actualizar un usuario existente"""
    try:
        usuario = obtener_usuario_por_id(db, usuario_id)
        
        if not usuario:
            return None
        
        # Actualizar solo los campos que vienen en la petición
        if usuario_data.username is not None:
            usuario.username = usuario_data.username.lower().strip()
        
        if usuario_data.password is not None:
            usuario.password = usuario_data.password  # Más adelante: hashear
        
        if usuario_data.rol is not None:
            usuario.rol = usuario_data.rol.lower().strip()
        
        if usuario_data.habilitado is not None:
            usuario.habilitado = usuario_data.habilitado
        
        if usuario_data.persona_id is not None:
            usuario.persona_id = usuario_data.persona_id
        
        if usuario_data.empresa_id is not None:
            usuario.empresa_id = usuario_data.empresa_id
        
        db.commit()
        db.refresh(usuario)
        
        return usuario
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: Ya existe otro usuario con ese username")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar usuario: {str(e)}")

# Eliminar usuario (cambiar habilitado a False en lugar de borrar físicamente)
def eliminar_usuario(db: Session, usuario_id: UUID) -> bool:
    """Eliminar un usuario (borrado lógico: cambia habilitado a False)"""
    try:
        usuario = obtener_usuario_por_id(db, usuario_id)
        
        if not usuario:
            return False
        
        # Borrado lógico: deshabilitar en lugar de eliminar
        usuario.habilitado = False
        db.commit()
        
        return True
        
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar usuario: {str(e)}")

# Borrado físico de usuario (si realmente se necesita)
def borrar_usuario_permanentemente(db: Session, usuario_id: UUID) -> bool:
    """Borrar usuario permanentemente (con cuidado)"""
    try:
        usuario = obtener_usuario_por_id(db, usuario_id)
        
        if not usuario:
            return False
        
        db.delete(usuario)
        db.commit()
        
        return True
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: No se puede eliminar el usuario porque tiene registros relacionados")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al borrar usuario: {str(e)}")