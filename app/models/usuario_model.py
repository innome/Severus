from passlib.context import CryptContext
import datetime
from typing import Optional
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioModel(BaseModel):
    username: str
    password: str
    rol: str = "usuario"
    fecha_registro: datetime.datetime = datetime.datetime.now()
    ultima_actualizacion: datetime.datetime = datetime.datetime.now()
    ultimo_login: Optional[datetime.datetime] = None  # Permite valores nulos
    estado: str = "activo"

    def hash_password(self):
        self.password = pwd_context.hash(self.password)

    def verificar_password(self, password: str):
        return pwd_context.verify(password, self.password)

class LoginRequest(BaseModel):
    username: str
    password: str