# app/repositories/__init__.py

from .persona import obtener_personas, obtener_persona_por_id, crear_persona
from .tipo_activo import (
    obtener_tipos_activo,
    obtener_tipo_activo_por_id,
    obtener_tipo_activo_por_nombre,
    crear_tipo_activo,
    actualizar_tipo_activo,
    eliminar_tipo_activo
)
from .empresa import (
    obtener_empresas,
    obtener_empresa_por_id,
    obtener_empresa_por_nit,
    obtener_empresa_por_nombre,
    crear_empresa,
    actualizar_empresa,
    eliminar_empresa
)