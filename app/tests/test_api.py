# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def sample_formulario():
    """Genera un payload de ejemplo que cumple con el modelo de FormularioTributarioModel."""
    return {
        "codigo_municipio": "TEST123",
        "url_pdf": "http://example.com/pdf",
        "calendario_tributario": "Calendario test 2023",
        "estatuto_tributario": [
            {"titulo": "Artículo 1", "contenido": "Contenido del artículo 1"}
        ],
        "ica": [
            {"titulo": "Artículo ICA 1", "contenido": "Contenido ICA 1"}
        ],
        "autoretencion_ica": [
            {"titulo": "Artículo Autoretención 1", "contenido": "Contenido Autoretención 1"}
        ],
        "fechas_ica": [
            {"0": "2023-01-01"},
            {"1": "2023-02-01"}
        ],
        "rete_ica": [
            {"titulo": "Artículo Rete 1", "contenido": "Contenido Rete 1"}
        ],
        "fechas_rete_ica": [
            {"0": "2023-03-01"},
            {"1": "2023-04-01"}
        ],
        "impuesto_industria_comercio": "Información Industria y Comercio",
        "periodicidad_impuestos": [
            {"tipo": "sas", "periodo": "anual"}
        ],
        "informacion_exogena_municipal_medios_magneticos": [
            {
                "titulo": "Medio 1",
                "ultimo_nit": [123],
                "fecha_pago": "2023-05-01",
                "fecha_vencimiento": "2023-06-01",
                "contenido": "Contenido del medio"
            }
        ],
        "vencimiento_declaraciones_x_nit": [
            {"0": "2023-07-01"}
        ],
        "vencimiento_declaraciones_x_nit_ica": [
            {"0": "2023-08-01"}
        ],
        "vencimiento_declaraciones_x_nit_rete_ica": [
            {"0": "2023-09-01"}
        ]
    }

def test_post_formulario_tributario():
    payload = sample_formulario()
    response = client.post("/informacion_tributaria/formulario_tributario", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "message" in data
    # Se espera que el mensaje confirme que el formulario fue procesado
    assert "Formulario procesado correctamente" in data["message"] or "Formulario tributario procesado correctamente" in data["message"]
    # Se verifica que se haya retornado la data con las claves esperadas
    result = data["data"]
    assert "impuestos" in result
    assert "calendario" in result
    assert "medios_magneticos" in result

def test_get_formulario_por_municipio():
    # Primero, insertar un formulario para un municipio específico
    payload = sample_formulario()
    payload["codigo_municipio"] = "TEST_MUNI"
    post_response = client.post("/informacion_tributaria/formulario_tributario", json=payload)
    assert post_response.status_code == 200, post_response.text
    
    # Obtener el formulario por municipio usando el endpoint correspondiente
    get_response = client.get("/formulario_tributario/municipio/TEST_MUNI")
    assert get_response.status_code == 200, get_response.text
    data = get_response.json()
    assert data["municipio"] == "TEST_MUNI"
    # Se verifica que existan al menos calendarios en la respuesta
    assert "calendarios" in data

def test_get_formulario_individual():
    # Insertar un formulario y obtener el id del calendario del resultado
    payload = sample_formulario()
    payload["codigo_municipio"] = "TEST_INDIV"
    post_response = client.post("/informacion_tributaria/formulario_tributario", json=payload)
    assert post_response.status_code == 200, post_response.text
    result = post_response.json()["data"]
    calendario_id = result["calendario"]
    
    # Obtener el formulario individual usando el id del calendario
    get_response = client.get(f"/formulario_tributario/{calendario_id}")
    assert get_response.status_code == 200, get_response.text
    individual_data = get_response.json()
    assert "calendario" in individual_data
    assert individual_data["calendario"]["id"] == calendario_id
