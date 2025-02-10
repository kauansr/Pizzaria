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
        'email': 'newuser@example.com',
        'password': 'newpassword'
    }
    response = client.post('/token', json=login_data)
    assert response.status_code == 200
    assert 'token' in response.json
    return response.json['token']

def test_create_user(client):
    """
    Test for creating a new user.

    Sends a POST request to the `/users` endpoint to create a new user
    and checks the response to ensure the user is created with valid fields.
    """
    user_data = {
        'email': 'newuser@example.com',
        'password': 'newpassword'
    }

    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    assert 'email' in response.json 
    assert 'create_at' in response.json
    assert response.json['email'] == user_data['email']

def test_find_user_without_token(client):
    """
    Test for finding a user without providing a JWT token.

    Sends a GET request to the `/users/<user_id>` endpoint without a token,
    expecting a `403 Forbidden` response status.
    """
    response = client.get('/users/1')
    assert response.status_code == 403 

def test_find_user_with_token(client):
    """
    Test for finding a user with a valid JWT token.

    Sends a POST request to create a user, then retrieves the user data with 
    a GET request to `/users/<user_id>` by providing a valid JWT token in the headers.
    """
    user_data = {
        'email': 'newuser@example.com',
        'password': 'newpassword'
    }

    response_create = client.post('/users', json=user_data)
    assert response_create.status_code == 201
    user_id = response_create.json['id']  

    token = get_jwt_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get(f'/users/{user_id}', headers=headers) 
    
    assert response.status_code == 200
    assert 'id' in response.json['user']
    assert 'email' in response.json['user']

def test_update_user(client):
    """
    Test for updating a user's details.

    Sends a PUT request to update a user's email and verifies that the update is successful.
    """
    user_data = {
        'email': 'newuser@example.com',
        'password': 'newpassword'
    }

    user_data_update = {
        'email': 'newuserupdated@example.com'
    }

    response_create = client.post('/users', json=user_data)
    assert response_create.status_code == 201
    user_id = response_create.json['id'] 

    token = get_jwt_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.put(f'/users/{user_id}', json=user_data_update, headers=headers)
    
    assert response.status_code == 200
    assert response.json == {}

def test_delete_user(client):
    """
    Test for deleting a user.

    Sends a DELETE request to remove a user by their ID, 
    then checks that the status code is `204 No Content`.
    """
    user_data = {
        'email': 'deleteuser@example.com',
        'password': 'deletepassword'
    }
    response_create = client.post('/users', json=user_data)
    user_id = response_create.json['id']
    
    token = get_jwt_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.delete(f'/users/{user_id}', headers=headers)
    assert response.status_code == 204

def test_login_user(client):
    """
    Test for logging in a user.

    Sends a POST request to the `/token` endpoint with user credentials 
    and verifies that the response contains a JWT token.
    """
    user_data = {
        'email': 'test@example.com',
        'password': 'password'
    }
    
    response_create = client.post('/users', json=user_data)
    assert response_create.status_code == 201  
    
    login_data = {
        'email': 'test@example.com',
        'password': 'password'
    }
    response_login = client.post('/token', json=login_data)
    
    assert response_login.status_code == 200 
    assert 'token' in response_login.json