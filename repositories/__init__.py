# app/repositories/__init__.py

from .persona import (
    obtener_personas,
    obtener_persona_por_id,
    obtener_persona_por_documento,
    obtener_persona_por_email,
    crear_persona,
    actualizar_persona,
    eliminar_persona
)
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

from .activo import (  # NUEVO
    obtener_activos,
    obtener_activo_por_id,
    obtener_activo_por_serial,
    obtener_activos_por_tipo,
    obtener_activos_por_empresa,
    obtener_activos_por_estado,
    crear_activo,
    actualizar_activo,
    eliminar_activo
)
from .usuario import (
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

from .ubicacion import (
    obtener_ubicaciones,
    obtener_ubicacion_por_id,
    obtener_ubicaciones_por_empresa,
    crear_ubicacion,
    actualizar_ubicacion
)

from .tecnico import (  
    obtener_tecnico_por_id,
    obtener_tecnico_por_persona,
    obtener_tecnicos_por_tipo,
    obtener_tecnicos_por_empresa,
    crear_tecnico,
    actualizar_tecnico
)

from .activo_ubicacion import (
    obtener_historial_por_activo,
    obtener_ubicacion_actual,
    crear_movimiento,
    retirar_ubicacion_actual
)

from .activo_relacion import (
    obtener_relaciones,
    obtener_relacion_por_id,
    obtener_relaciones_por_padre,
    obtener_relaciones_por_hijo,
    obtener_relaciones_activas,
    existe_relacion_activa,
    crear_relacion,
    finalizar_relacion,
)