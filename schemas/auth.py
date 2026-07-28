from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UsuarioLogin(BaseModel):
    """Para autenticación"""
    username: str
    password: str