import os
import sys
import pytest
from fastapi.testclient import TestClient

# Establecer variable de entorno para testing
os.environ["TESTING"] = "1"

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Importar la base de datos y sobrescribir la conexión
from app.config.database import database
from tests.dummies import DummyDatabase

async def fake_connect():
    print("TESTING mode: using DummyDatabase.")
    database.client = None
    database.db = DummyDatabase()

async def fake_disconnect():
    print("TESTING mode: disconnecting DummyDatabase.")
    database.client = None
    database.db = None

database.connect = fake_connect
database.disconnect = fake_disconnect

# Importar la app después de haber sobrescrito la conexión
from app.main import app
from config.auth import get_current_user
from models.usuario_model import UsuarioModel

# Sobrescribir métodos de hash para evitar bcrypt en tests
def fake_hash_password(self):
    pass

UsuarioModel.hash_password = fake_hash_password
UsuarioModel.verificar_password = lambda self, password: self.password == password

def override_get_current_user():
    return {"username": "testuser", "role": "user"}

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
