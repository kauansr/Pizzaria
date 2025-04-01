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


def test_create_produto(client):
    """
    Test for creating a new product.
    Sends a POST request to create a new product and checks the response.
    """
    produto_data = {"nome": "Produto Teste", "preco": 99.99}

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/produto", json=produto_data, headers=headers)

    assert response.status_code == 201
    assert response.json["nome"] == produto_data["nome"]
    assert response.json["preco"] == produto_data["preco"]


def test_find_produto(client):
    """
    Test for retrieving a product by ID.
    Creates a product and retrieves it using a GET request.
    """
    produto_data = {"nome": "Produto Teste", "preco": 99.99}

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create product
    response_create = client.post("/produto", json=produto_data, headers=headers)
    assert response_create.status_code == 201
    produto_id = response_create.json["id"]

    # Retrieve the product
    response = client.get(f"/produto/{produto_id}", headers=headers)

    assert response.status_code == 200
    assert "nome" in response.json["produto"]
    assert "preco" in response.json["produto"]
    assert response.json["produto"]["nome"] == produto_data["nome"]
    assert response.json["produto"]["preco"] == produto_data["preco"]


def test_update_produto(client):
    """
    Test for updating a product's details.
    Creates a product, then updates it with new information.
    """
    produto_data = {"nome": "Produto Teste", "preco": 99.99}

    produto_data_update = {"nome": "Produto Atualizado", "preco": 199.99}

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create product
    response_create = client.post("/produto", json=produto_data, headers=headers)
    assert response_create.status_code == 201
    produto_id = response_create.json["id"]

    # Update product
    response_update = client.put(
        f"/produto/{produto_id}", json=produto_data_update, headers=headers
    )

    assert response_update.status_code == 200
    assert response_update.json == {}

    # Verify the update by retrieving the product again
    response_find = client.get(f"/produto/{produto_id}", headers=headers)
    assert response_find.status_code == 200
    assert response_find.json["produto"]["nome"] == produto_data_update["nome"]
    assert response_find.json["produto"]["preco"] == produto_data_update["preco"]


def test_delete_produto(client):
    """
    Test for deleting a product by ID.
    Creates a product and deletes it using a DELETE request.
    """
    produto_data = {"nome": "Produto Teste", "preco": 99.99}

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create product
    response_create = client.post("/produto", json=produto_data, headers=headers)
    assert response_create.status_code == 201
    produto_id = response_create.json["id"]

    # Delete product
    response_delete = client.delete(f"/produto/{produto_id}", headers=headers)
    assert response_delete.status_code == 204

    # Verify deletion by trying to retrieve the product
    response_find = client.get(f"/produto/{produto_id}", headers=headers)
    assert response_find.status_code == 404


def test_find_produto_without_token(client):
    """
    Test for retrieving a product without providing a token.
    Sends a GET request to retrieve a product and expects a `200 OK` response
    since the company is a superadmin and doesn't need an extra token.
    """
    produto_data = {"nome": "Produto Teste", "preco": 99.99}

    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create product
    response_create = client.post("/produto", json=produto_data, headers=headers)
    assert response_create.status_code == 201
    produto_id = response_create.json["id"]

    # Retrieve product without token - expecting success since empresa is superadmin
    response_find = client.get(f"/produto/{produto_id}")

    assert response_find.status_code == 200
    assert "nome" in response_find.json["produto"]
    assert "preco" in response_find.json["produto"]
    assert response_find.json["produto"]["nome"] == produto_data["nome"]
    assert response_find.json["produto"]["preco"] == produto_data["preco"]
