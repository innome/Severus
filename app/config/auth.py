import os
from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

# Configuración: Se puede definir o usar SECRET_KEY desde jwt_alternative.py, pero en este ejemplo
# lo dejamos definido aquí para claridad.
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# Importamos nuestras funciones de jwt_alternative
from config.jwt_alternative import create_token, verify_token

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token JWT usando la función create_token de nuestra librería alternativa.
    """
    return create_token(data, expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def verify_jwt_token(token: str):
    try:
        payload = verify_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o incompleto",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Retornamos un diccionario con la información del usuario (puedes agregar más campos)
        return {"username": username, "role": "user"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: " + str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_jwt_token(token)
