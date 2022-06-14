def test_keycloak_auth_endpoint(client):

    response = client.get("/api/keycloak_auth")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}
