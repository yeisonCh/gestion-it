from sqlalchemy.orm import Session

from repositories.usuario import obtener_usuario_por_username
from auth.password_handler import verify_password
from auth.jwt_handler import create_access_token

def autenticar_usuario(
    db: Session,
    username: str,
    password: str
):
    usuario = obtener_usuario_por_username(db, username)

    if not usuario:
        return None

    if not verify_password(password, usuario.password):
        return None

    if not usuario.habilitado:
        return None

    return {
        "access_token": create_access_token({"sub": usuario.username}),
        "token_type": "bearer"
    }