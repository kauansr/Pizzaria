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
    login_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123'
    }
    response = client.post('/empresa/token', json=login_data)
    assert response.status_code == 200
    assert 'token' in response.json
    return response.json['token']

def test_create_empresa(client):
    """
    Test for creating a new company.

    Sends a POST request to the `/empresa` endpoint to create a new company,
    then checks the response to ensure the company is created with the correct fields.
    """
    empresa_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123',
        'cnpj': '12.345.678/0001-99'
    }

    response = client.post('/empresa', json=empresa_data)
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['owner_email'] == empresa_data['email']
    assert response.json['cnpj'] == empresa_data['cnpj']

def test_find_empresa_without_token(client):
    """
    Test for retrieving a company without providing a token.

    Sends a GET request to the `/empresa/<empresa_id>` endpoint without a token,
    expecting a `403 Forbidden` response status.
    """
    response = client.get('/empresa/1')
    assert response.status_code == 403

def test_find_empresa_with_token(client):
    """
    Test for retrieving a company with a valid token.

    Sends a POST request to create a company, then retrieves the company data with 
    a GET request to `/empresa/<empresa_id>` by providing a valid JWT token in the headers.
    """
    empresa_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123',
        'cnpj': '12.345.678/0001-99'
    }

    response_create = client.post('/empresa', json=empresa_data)
    assert response_create.status_code == 201
    empresa_id = response_create.json['id']
    
    token = get_jwt_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get(f'/empresa/{empresa_id}', headers=headers)
    
    assert response.status_code == 200
    assert 'id' in response.json['empresa']
    assert 'email' in response.json['empresa']

def test_update_empresa(client):
    """
    Test for updating a company's details.

    Sends a PUT request to update a company's email and CNPJ, 
    then verifies that the update is successful.
    """
    empresa_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123',
        'cnpj': '12.345.678/0001-99'
    }

    empresa_data_update = {
        'email': 'company@new.com',
        'cnpj': '98.765.432/0001-00'
    }

    response_create = client.post('/empresa', json=empresa_data)
    assert response_create.status_code == 201
    empresa_id = response_create.json['id']
    
    token = get_jwt_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.put(f'/empresa/{empresa_id}', json=empresa_data_update, headers=headers)
    
    assert response.status_code == 200
    assert response.json == {}

def test_delete_empresa(client):
    """
    Test for deleting a company.

    Sends a DELETE request to remove a company by its ID, 
    then checks that the status code is `204 No Content`.
    """
    empresa_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123',
        'cnpj': '12.345.678/0001-99'
    }

    response_create = client.post('/empresa', json=empresa_data)
    empresa_id = response_create.json['id']
    
    token = get_jwt_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.delete(f'/empresa/{empresa_id}', headers=headers)
    assert response.status_code == 204

def test_login_empresa(client):
    """
    Test for logging in a company.

    Sends a POST request to the `/empresa/token` endpoint with company credentials 
    and verifies that the response contains a JWT token.
    """
    empresa_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123',
        'cnpj': '12.345.678/0001-99'
    }
    
    response_create = client.post('/empresa', json=empresa_data)
    assert response_create.status_code == 201  
    
    login_data = {
        'email': 'company@example.com',
        'password': 'SecurePassword123'
    }
    response_login = client.post('/empresa/token', json=login_data)
    
    assert response_login.status_code == 200 
    assert 'token' in response_login.json