def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert "message" in json_data
    # Verificamos que el mensaje incluya la cadena de confirmación
    assert "FastAPI está funcionando" in json_data["message"]
