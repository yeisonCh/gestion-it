# app/schemas/empresa.py

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from uuid import UUID
import re

class EmpresaCrear(BaseModel):
    nombre: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        description="Nombre de la empresa",
        example="Tecnología SAS"
    )
    nit: str = Field(
        ..., 
        min_length=5, 
        max_length=20,
        description="NIT de la empresa (solo números o con dígito de verificación)",
        example="901234567"
    )
    direccion: Optional[str] = Field(
        None, 
        max_length=200,
        description="Dirección física",
        example="Calle 123 #45-67"
    )
    telefono: Optional[str] = Field(
        None, 
        max_length=20,
        description="Teléfono de contacto",
        example="3001234567"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Correo electrónico",
        example="contacto@empresa.com"
    )
    sede: Optional[str] = Field(
        None, 
        max_length=100,
        description="Nombre de la sede principal",
        example="Sede Central"
    )
    
    # Validadores
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre de la empresa no puede estar vacío')
        
        v = v.strip().upper()
        
        # Permitir letras, números, espacios, y caracteres comerciales (&, ., etc)
        if not re.match(r'^[A-Za-z0-9\s\&\-\.]+$', v):
            raise ValueError('El nombre solo puede contener letras, números, espacios, &, - y .')
        
        if '  ' in v:
            raise ValueError('El nombre no puede tener espacios dobles')
        
        return v
    
    @field_validator('nit')
    @classmethod
    def validar_nit(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El NIT no puede estar vacío')
        
        v = v.strip()
        
        # CORREGIDO: Validación flexible
        # Permite: solo números (ej: 901234567) o con guión (ej: 901234567-1)
        if not re.match(r'^\d{6,15}(-\d{1,2})?$', v):
            raise ValueError('El NIT debe contener solo números, opcionalmente con guión y 1-2 dígitos')
        
        return v
    
    @field_validator('telefono')
    @classmethod
    def validar_telefono(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        
        if not v.strip():
            return None
        
        # Eliminar espacios y formatear
        v = v.strip()
        
        # Solo números y símbolos de teléfono
        if not re.match(r'^[\d\+\-\s\(\)]+$', v):
            raise ValueError('El teléfono solo puede contener números, +, -, espacios y ()')
        
        return v


class EmpresaActualizar(BaseModel):
    """Para actualizar empresa (todos los campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    nit: Optional[str] = Field(None, min_length=5, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    sede: Optional[str] = Field(None, max_length=100)
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().upper()
    
    @field_validator('nit')
    @classmethod
    def validar_nit(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('El NIT no puede estar vacío')
        if not re.match(r'^\d{6,10}-\d$', v.strip()):
            raise ValueError('El NIT debe tener formato: XXXXXX-X')
        return v.strip()


class EmpresaRespuesta(BaseModel):
    """Respuesta de empresa (lo que se devuelve al cliente)"""
    id: UUID
    nombre: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sede: Optional[str] = None

    class Config:
        from_attributes = True  # SQLAlchemy to Pydantic