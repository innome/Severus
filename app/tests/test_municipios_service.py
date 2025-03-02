import pytest
import unicodedata
from models.municipios_model import MunicipioModel
from services.municipios_service import (
    obtener_todos_los_municipios,
    buscar_municipio_por_codigo,
    buscar_municipios_por_nombre,
    eliminar_diacriticos,
)

# --- Dummy para simular el cursor asíncrono ---
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

# --- DummyCollection para simular la colección de MongoDB ---
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
            # Búsqueda simple case-insensitive
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

# Fixture que provee el dummy de la colección
@pytest.fixture
def dummy_collection():
    return DummyCollection()

# Sobrescribir la función get_collection en el módulo de municipios_service
@pytest.fixture(autouse=True)
def override_get_collection(monkeypatch, dummy_collection):
    monkeypatch.setattr(
        "services.municipios_service.get_collection", lambda name: dummy_collection
    )

@pytest.mark.asyncio
async def test_obtener_todos_los_municipios(dummy_collection):
    # Preinsertar documentos dummy con el campo 'nombre_normalizado'
    docs = [
        {"codigo_municipio": "001", "nombre": "Bogotá", "nombre_normalizado": "Bogota"},
        {"codigo_municipio": "002", "nombre": "Medellín", "nombre_normalizado": "Medellin"},
    ]
    dummy_collection.docs.extend(docs)

    municipios = await obtener_todos_los_municipios(skip=0)
    assert len(municipios) == 2
    assert municipios[0].codigo_municipio == "001"
    assert municipios[1].codigo_municipio == "002"

@pytest.mark.asyncio
async def test_buscar_municipio_por_codigo(dummy_collection):
    doc = {"codigo_municipio": "003", "nombre": "Cali", "nombre_normalizado": "Cali"}
    dummy_collection.docs.append(doc)

    municipio = await buscar_municipio_por_codigo("003")
    assert municipio is not None
    assert municipio.codigo_municipio == "003"

    # Búsqueda de código inexistente retorna None
    municipio_none = await buscar_municipio_por_codigo("999")
    assert municipio_none is None

def test_eliminar_diacriticos():
    texto = "áéíóú ÁÉÍÓÚ ñ Ñ"
    # Eliminar diacríticos
    resultado = eliminar_diacriticos(texto)
    # Para simplificar, se espera que las vocales tildadas se reemplacen por sin tilde
    esperado = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    assert resultado == esperado

@pytest.mark.asyncio
async def test_buscar_municipios_por_nombre(dummy_collection):
    # Insertamos varios documentos con el campo 'nombre_normalizado'
    docs = [
        {"codigo_municipio": "004", "nombre": "Bucaramanga", "nombre_normalizado": "Bucaramanga"},
        {"codigo_municipio": "005", "nombre": "Bucaramánga", "nombre_normalizado": "Bucaramanga"},
        {"codigo_municipio": "006", "nombre": "Pereira", "nombre_normalizado": "Pereira"},
    ]
    dummy_collection.docs.extend(docs)

    # Buscamos por nombre sin diacríticos
    municipios = await buscar_municipios_por_nombre("Bucaramanga")
    assert len(municipios) == 2

    # Buscamos por un nombre que no exista
    municipios_none = await buscar_municipios_por_nombre("NonExistente")
    assert municipios_none == []
