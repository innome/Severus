import pytest
from fastapi.testclient import TestClient
from app.main import app

# --- Reutilizamos las clases DummyCursor y DummyCollection ---
class DummyCursor:
    def __init__(self, docs):
        self.docs = docs
        self.index = 0

    def skip(self, n: int):
        self.docs = self.docs[n:]
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.docs):
            raise StopAsyncIteration
        doc = self.docs[self.index]
        self.index += 1
        return doc

class DummyCollection:
    def __init__(self):
        self.docs = []

    async def insert_one(self, doc):
        self.docs.append(doc)
        class Result:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id

        return Result(inserted_id=str(len(self.docs)))

    def find(self, query: dict = None):
        if query and "nombre_normalizado" in query:
            regex = query["nombre_normalizado"]["$regex"]
            filtered = [
                doc
                for doc in self.docs
                if regex.lower() in doc.get("nombre_normalizado", "").lower()
            ]
        else:
            filtered = self.docs
        return DummyCursor(filtered)

    async def find_one(self, query: dict):
        for doc in self.docs:
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

# Sobrescribir get_collection en el módulo del servicio de municipios
@pytest.fixture(autouse=True)
def override_get_collection(monkeypatch, dummy_collection):
    monkeypatch.setattr(
        "services.municipios_service.get_collection", lambda name: dummy_collection
    )

# Prepopular el dummy con datos para los tests de los endpoints
@pytest.fixture(autouse=True)
def prepopulate_dummy_collection(dummy_collection):
    # Se limpian y agregan documentos de prueba
    dummy_collection.docs.clear()
    docs = [
        {"codigo_municipio": "001", "nombre": "Bogotá", "nombre_normalizado": "Bogota"},
        {"codigo_municipio": "002", "nombre": "Medellín", "nombre_normalizado": "Medellin"},
        {"codigo_municipio": "003", "nombre": "Cali", "nombre_normalizado": "Cali"},
    ]
    dummy_collection.docs.extend(docs)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_listar_municipios(client):
    # GET /municipios/?skip=0
    response = client.get("/municipios/?skip=0")
    assert response.status_code == 200
    data = response.json()
    # Esperamos los 3 documentos preinsertados
    assert isinstance(data, list)
    assert len(data) == 3

def test_obtener_municipio_existente(client):
    # GET /municipios/001
    response = client.get("/municipios/001")
    assert response.status_code == 200
    data = response.json()
    assert data["codigo_municipio"] == "001"
    assert "nombre" in data

def test_obtener_municipio_inexistente(client):
    # GET /municipios/999 debería retornar 404
    response = client.get("/municipios/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Municipio no encontrado"

def test_buscar_municipios_por_nombre_existente(client):
    # GET /municipios/buscar/?nombre=Medellin
    response = client.get("/municipios/buscar/?nombre=Medellin")
    assert response.status_code == 200
    data = response.json()
    # Se espera que retorne el municipio Medellín (sin tilde en el campo normalizado)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["codigo_municipio"] == "002"

def test_buscar_municipios_por_nombre_inexistente(client):
    # GET /municipios/buscar/?nombre=NonExistente
    response = client.get("/municipios/buscar/?nombre=NonExistente")
    # El endpoint define que si no hay resultados se lanza HTTPException 404
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No se encontraron municipios con ese nombre"
