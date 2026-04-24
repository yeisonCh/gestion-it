# app/services/__init__.py

from .persona import service_obtener_personas, service_obtener_persona_por_id, service_crear_persona
from .tipo_activo import (
    service_obtener_tipos_activo,
    service_obtener_tipo_activo_por_id,
    service_crear_tipo_activo,
    service_actualizar_tipo_activo,
    service_eliminar_tipo_activo
)
from .empresa import (
    service_obtener_empresas,
    service_obtener_empresa_por_id,
    service_crear_empresa,
    service_actualizar_empresa,
    service_eliminar_empresa
)