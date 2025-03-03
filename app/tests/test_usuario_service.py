import pytest
from models.usuario_model import UsuarioModel
from services.usuario_service import crear_usuario, obtener_usuario_por_username, verificar_credenciales

# Dummy de la colección para simular operaciones en la base de datos
class DummyCollection:
    def __init__(self):
        self.storage = {}
        self.counter = 1

    async def insert_one(self, doc):
        inserted_id = str(self.counter)
        self.storage[inserted_id] = doc
        self.counter += 1
        # Se pasa el valor inserted_id al constructor de Result
        class Result:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return Result(inserted_id)

    async def find_one(self, query):
        for doc in self.storage.values():
            match = True
            for key, value in query.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                return doc
        return None

@pytest.fixture
def dummy_collection():
    return DummyCollection()

# Sobrescribir la función get_collection en el módulo de servicios
@pytest.fixture(autouse=True)
def override_get_collection(monkeypatch, dummy_collection):
    monkeypatch.setattr("services.usuario_service.get_collection", lambda name: dummy_collection)

@pytest.mark.asyncio
async def test_crear_usuario():
    user = UsuarioModel(username="testuser", password="secret")
    user_id = await crear_usuario(user)
    # El primer id insertado debe ser "1"
    assert user_id == "1"

@pytest.mark.asyncio
async def test_obtener_usuario_por_username(dummy_collection):
    # Preinserta un usuario en la colección dummy
    user = UsuarioModel(username="john", password="secret")
    user.hash_password()  # En tests no se realiza hashing real (se sobreescribe en conftest)
    dummy_collection.storage["1"] = user.dict()
    
    fetched_user = await obtener_usuario_por_username("john")
    assert fetched_user is not None
    assert fetched_user.username == "john"

@pytest.mark.asyncio
async def test_verificar_credenciales(dummy_collection):
    # Inserta un usuario con contraseña conocida
    user = UsuarioModel(username="alice", password="mypassword")
    user.hash_password()
    dummy_collection.storage["1"] = user.dict()

    # Prueba con la contraseña correcta
    valid_user = await verificar_credenciales("alice", "mypassword")
    assert valid_user is not None
    assert valid_user.username == "alice"

    # Prueba con contraseña incorrecta
    invalid_user = await verificar_credenciales("alice", "wrongpassword")
    assert invalid_user is None
