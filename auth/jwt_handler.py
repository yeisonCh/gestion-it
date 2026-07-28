import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv

# Clave secreta para firmar los tokens
# Más adelante la moveremos al archivo .env
SECRET_KEY = os.getenv("SECRET_KEY")

# Algoritmo de cifrado
ALGORITHM = os.getenv("ALGORITHM")

# Tiempo de vida del token (minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)


def create_access_token(data: dict):
    """
    Genera un token JWT.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(token: str):
    """
    Verifica que el token sea válido y devuelve su contenido.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None