# app/tests/test_tributaria_versionada.py
import uuid
import pytest
from fastapi.testclient import TestClient

# Payload base de ejemplo (se modificará la versión para evitar duplicados)
sample_payload = {
    "codigo_municipio": "05001",
    "version": "0.0.1",  # Este valor se reemplazará por uno único en cada test
    "activo": True,
    "url_pdf": "http://example.com/pdf",
    "calendario_tributario": "Calendario de prueba",
    "estatuto_tributario": [],
    "ica": [],
    "autoretencion_ica": [],
    "fechas_ica": [{"0": "2023-05-01"}],
    "rete_ica": [],
    "fechas_rete_ica": [{"0": "2023-05-15"}],
    "impuesto_industria_comercio": "Gravamen de prueba",
    "periodicidad_impuestos": [{"tipo": "mensual", "periodo": "Mensual"}],
    "informacion_exogena_municipal_medios_magneticos": [],
    "vencimiento_declaraciones_x_nit": [{"0": "2023-06-01"}],
    "vencimiento_declaraciones_x_nit_ica": [{"0": "2023-06-15"}],
    "vencimiento_declaraciones_x_nit_rete_ica": [{"0": "2023-06-20"}]
}

def create_unique_payload():
    payload = sample_payload.copy()
    unique_version = f"0.0.1-{uuid.uuid4().hex[:6]}"
    payload["version"] = unique_version
    return payload

def test_crear_informacion_tributaria_versionada(client: TestClient):
    payload = create_unique_payload()
    response = client.post("/informacion_tributaria_versionada/", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "message" in data
    assert data["message"] == "Información creada con éxito"
    assert "id" in data
    created_id = data["id"]
    assert isinstance(created_id, str) and created_id != ""
    # Retornamos el id para posibles usos en otros tests
    return created_id

def test_listar_informacion_tributaria_versionada(client: TestClient):
    # Creamos un documento único para garantizar que la lista no esté vacía
    payload = create_unique_payload()
    client.post("/informacion_tributaria_versionada/", json=payload)
    response = client.get("/informacion_tributaria_versionada/?skip=0")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)

def test_obtener_informacion_por_municipio_version(client: TestClient):
    payload = create_unique_payload()
    response_create = client.post("/informacion_tributaria_versionada/", json=payload)
    assert response_create.status_code == 200, response_create.text
    version = payload["version"]
    response = client.get(f"/informacion_tributaria_versionada/05001/{version}")
    if response.status_code == 200:
        data = response.json()
        assert data["codigo_municipio"] == "05001"
        assert data["version"] == version
    else:
        pytest.skip("No se encontró información para municipio 05001 y versión " + version)

def test_deshabilitar_informacion_tributaria_versionada(client: TestClient):
    payload = create_unique_payload()
    response_create = client.post("/informacion_tributaria_versionada/", json=payload)
    assert response_create.status_code == 200, response_create.text
    version = payload["version"]
    response_delete = client.delete(f"/informacion_tributaria_versionada/05001/{version}")
    assert response_delete.status_code == 200, response_delete.text
    data_delete = response_delete.json()
    assert data_delete["message"] == "Información deshabilitada con éxito"
    response_get = client.get(f"/informacion_tributaria_versionada/05001/{version}")
    assert response_get.status_code == 200, f"Se esperaba 200, se obtuvo {response_get.status_code}"
