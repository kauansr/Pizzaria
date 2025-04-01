from src.main.server.server import create_app
import pytest


@pytest.fixture
def client():
    """
    Fixture for initializing the test client.
    Creates an instance of the Flask app and provides a test client for API calls.
    """
    app = create_app()
    with app.test_client() as client:
        yield client


def get_jwt_token(client):
    """
    Helper function to get a JWT token for login.

    Simulates a login request, receives a JWT token in response,
    and returns it to be used for authenticated requests.
    """
    login_data = {"email": "company@example.com", "password": "SecurePassword123"}
    response = client.post("/empresa/token", json=login_data)
    assert response.status_code == 200
    assert "token" in response.json
    return response.json["token"]


def test_create_pedido(client):
    """
    Test for creating a new pedido.
    Sends a POST request to create a new pedido and checks the response.
    """
    pedido_data = {
        "user_id": 1,
        "email": "customer@example.com",
        "nome": "Pedido Teste",
        "frete": 10.0,
        "custo_total": 100.0,
    }

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/pedido", json=pedido_data, headers=headers)

    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["pedido_nome"] == pedido_data["nome"]
    assert response.json["frete"] == pedido_data["frete"]
    assert response.json["custo_total"] == pedido_data["custo_total"]


def test_find_pedido(client):
    """
    Test for retrieving a pedido by ID.
    Creates a pedido and retrieves it using a GET request.
    """
    pedido_data = {
        "user_id": 1,
        "email": "customer@example.com",
        "nome": "Pedido Teste",
        "frete": 10.0,
        "custo_total": 100.0,
    }

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create pedido
    response_create = client.post("/pedido", json=pedido_data, headers=headers)
    assert response_create.status_code == 201
    pedido_id = response_create.json["id"]

    # Retrieve the pedido
    response = client.get(f"/pedido/{pedido_id}", headers=headers)

    assert response.status_code == 200
    assert "pedido" in response.json
    assert response.json["pedido"]["nome"] == pedido_data["nome"]
    assert response.json["pedido"]["frete"] == pedido_data["frete"]
    assert response.json["pedido"]["custo_total"] == pedido_data["custo_total"]


def test_update_pedido(client):
    """
    Test for updating a pedido's details.
    Creates a pedido, then updates it with new information.
    """
    pedido_data = {
        "user_id": 1,
        "email": "customer@example.com",
        "nome": "Pedido Teste",
        "frete": 10.0,
        "custo_total": 100.0,
    }

    pedido_data_update = {
        "status_pedido": "Enviado",
    }

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create pedido
    response_create = client.post("/pedido", json=pedido_data, headers=headers)
    assert response_create.status_code == 201
    pedido_id = response_create.json["id"]

    # Update pedido
    response_update = client.put(
        f"/pedido/{pedido_id}", json=pedido_data_update, headers=headers
    )

    assert response_update.status_code == 200
    assert response_update.json == {}

    # Verify the update by retrieving the pedido again
    response_find = client.get(f"/pedido/{pedido_id}", headers=headers)
    assert response_find.status_code == 200


def test_delete_pedido(client):
    """
    Test for deleting a pedido by ID.
    Creates a pedido and deletes it using a DELETE request.
    """
    pedido_data = {
        "user_id": 1,
        "email": "customer@example.com",
        "nome": "Pedido Teste",
        "frete": 10.0,
        "custo_total": 100.0,
    }

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create pedido
    response_create = client.post("/pedido", json=pedido_data, headers=headers)
    assert response_create.status_code == 201
    pedido_id = response_create.json["id"]

    # Delete pedido
    response_delete = client.delete(f"/pedido/{pedido_id}", headers=headers)
    assert response_delete.status_code == 204

    # Verify deletion by trying to retrieve the pedido
    response_find = client.get(f"/pedido/{pedido_id}", headers=headers)
    assert response_find.status_code == 404


def test_find_pedido_without_token(client):
    """
    Test for retrieving a pedido without providing a token.
    Expects a 403 Forbidden response because the route requires authentication.
    """
    pedido_data = {
        "user_id": 1,
        "email": "customer@example.com",
        "nome": "Pedido Teste",
        "frete": 10.0,
        "custo_total": 100.0,
    }

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create pedido
    response_create = client.post("/pedido", json=pedido_data, headers=headers)
    assert response_create.status_code == 201
    pedido_id = response_create.json["id"]

    # Retrieve pedido without token
    response_find = client.get(f"/pedido/{pedido_id}")  # No token sent here

    assert response_find.status_code == 403  # Forbidden
