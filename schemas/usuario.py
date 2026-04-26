# app/schemas/usuario.py

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from uuid import UUID
import re

# Enum para roles (como en .NET)
class RolUsuario(str):
    ADMIN = "admin"
    OPERATIVO = "operativo"

class UsuarioCrear(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre de usuario único",
        example="jperez"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Contraseña (mínimo 6 caracteres)",
        example="miPassword123"
    )
    rol: str = Field(
        ...,
        description="Rol del usuario: admin o operativo",
        example="operativo"
    )
    habilitado: bool = Field(
        default=True,
        description="Si el usuario está habilitado"
    )
    persona_id: UUID = Field(
        ...,
        description="ID de la persona asociada"
    )
    empresa_id: UUID = Field(
        ...,
        description="ID de la empresa asociada"
    )
    
    @field_validator('username')
    @classmethod
    def validar_username(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre de usuario no puede estar vacío')
        
        v = v.strip().lower()
        
        # Solo letras, números y guión bajo
        if not re.match(r'^[a-z0-9_]+$', v):
            raise ValueError('El username solo puede contener letras minúsculas, números y guión bajo')
        
        return v
    
    @field_validator('password')
    @classmethod
    def validar_password(cls, v: str) -> str:
        if not v or len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v
    
    @field_validator('rol')
    @classmethod
    def validar_rol(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in ['admin', 'operativo']:
            raise ValueError('El rol debe ser "admin" o "operativo"')
        return v


class UsuarioActualizar(BaseModel):
    """Para actualizar usuario (todos los campos opcionales)"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    rol: Optional[str] = None
    habilitado: Optional[bool] = None
    persona_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    
    @field_validator('username')
    @classmethod
    def validar_username(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('El nombre de usuario no puede estar vacío')
        return v.strip().lower()
    
    @field_validator('rol')
    @classmethod
    def validar_rol(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().lower()
        if v not in ['admin', 'operativo']:
            raise ValueError('El rol debe ser "admin" o "operativo"')
        return v


class UsuarioRespuesta(BaseModel):
    """Respuesta de usuario (sin password por seguridad)"""
    id: UUID
    username: str
    rol: str
    habilitado: bool
    persona_id: UUID
    empresa_id: UUID
    
    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """Para autenticación"""
    username: str
    password: str