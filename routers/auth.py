from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth import Token, UsuarioLogin
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import autenticar_usuario

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Autenticar usuario"
)
def login(
    login_data: UsuarioLogin,
    db: Session = Depends(get_db)
):
    resultado = autenticar_usuario(
        db=db,
        username=login_data.username,
        password=login_data.password
    )

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    return resultado