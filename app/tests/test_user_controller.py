import pytest
from fastapi.testclient import TestClient
from app.main import app

# Funciones fake para simular la lógica de los servicios en el controlador
async def fake_verificar_credenciales(username: str, password: str):
    # Si el usuario es "existing", simulamos que ya existe
    if username == "existing":
        from models.usuario_model import UsuarioModel
        return UsuarioModel(username=username, password=password)
    # Para el login, si el usuario es "valid" retornamos un usuario dummy
    if username == "valid":
        from models.usuario_model import UsuarioModel
        user = UsuarioModel(username=username, password=password)
        user.password = "hashedpassword"
        return user
    return None

async def fake_crear_usuario(usuario):
    return "dummy_id"

def fake_create_access_token(data, expires_delta):
    return "fake_token"

# Sobrescribir las funciones en el módulo del controlador (se usa la ruta de importación en el controlador)
@pytest.fixture(autouse=True)
def override_service_functions(monkeypatch):
    monkeypatch.setattr("controllers.user_controller.verificar_credenciales", fake_verificar_credenciales)
    monkeypatch.setattr("controllers.user_controller.crear_usuario", fake_crear_usuario)
    monkeypatch.setattr("controllers.user_controller.create_access_token", fake_create_access_token)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_registrar_usuario_existente(client):
    # Se intenta registrar un usuario que ya existe (username "existing")
    payload = {"username": "existing", "password": "secret"}
    response = client.post("/usuarios/registro", json=payload)
    # Se espera error 400
    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario ya existe"

def test_registrar_usuario_exitoso(client):
    # Registro exitoso de un nuevo usuario
    payload = {"username": "newuser", "password": "secret"}
    response = client.post("/usuarios/registro", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Usuario registrado exitosamente"
    assert data["id"] == "dummy_id"

def test_login_usuario_valido(client):
    # Inicio de sesión con credenciales válidas (username "valid")
    form_data = {"username": "valid", "password": "any"}
    response = client.post("/usuarios/login", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake_token"
    assert data["token_type"] == "bearer"

def test_login_usuario_invalido(client):
    # Inicio de sesión con credenciales inválidas
    form_data = {"username": "nonexistent", "password": "wrong"}
    response = client.post("/usuarios/login", data=form_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"

def test_ruta_protegida(client):
    # La ruta protegida debe retornar 200 (ya que get_current_user se sobreescribe en conftest)
    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Solo usuarios autenticados pueden acceder a esta ruta"
