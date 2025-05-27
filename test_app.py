# Import the Flask app from app.py
from app import app

# Import pytest to use its testing features
import pytest

# This is a pytest fixture that provides a test client for Flask
@pytest.fixture
def client():
    # Flask provides a test client for simulating HTTP requests
    with app.test_client() as client:
        yield client  # Yield the client so test functions can use it

# Test case 1: Successfully create a new user
def test_create_user(client):
    print('🔄 test_create_user: Sending POST request to /users...')

    # Send POST request with a JSON body containing a 'name'
    response = client.post('/users', json={'name': 'Alice'})
    print('response = client.post("/users", json={"name": "Alice"})')

    # Expecting HTTP 201 Created
    assert response.status_code == 201
    print('✅ Received 201 Created')

    # Extract JSON data from response
    data = response.get_json()

    # The response should include a "user" with the correct name
    assert data['user']['name'] == 'Alice'
    print('✅ User created with name:', data['user']['name'])

# Test case 2: Fail when creating a user without a required field
def test_create_user_missing_field(client):
    print('🔄 test_create_user_missing_field: Sending POST with no name...')

    # Send POST request without a 'name' field
    response = client.post('/users', json={})
    print('response = client.post("/users", json={})')

    # Expecting HTTP 400 Bad Request
    assert response.status_code == 400
    print('✅ Correctly failed with 400 Bad Request')

# Test case 3: Get an existing user by ID
def test_get_user(client):
    print('🔄 test_get_user: Creating then fetching user...')

    # First, create a user
    post_response = client.post('/users', json={'name': 'Bob'})
    print('post_response = client.post("/users", json={"name": "Bob"})')

    # Extract the ID from the response
    user_id = post_response.get_json()['user_id']
    print('user_id = post_response.get_json()["user_id"]')

    # Retrieve the user by their ID
    get_response = client.get(f'/users/{user_id}')
    print(f'get_response = client.get("/users/{user_id}")')

    # Expecting HTTP 200 OK
    assert get_response.status_code == 200
    print('✅ Retrieved user with status 200')

    # Verify the name matches what we created
    assert get_response.get_json()['name'] == 'Bob'
    print('✅ Retrieved user has name:', get_response.get_json()['name'])

# Test case 4: Try to get a user that doesn't exist
def test_get_user_not_found(client):
    print('🔄 test_get_user_not_found: Fetching non-existent user...')

    # Try to fetch a user ID that doesn't exist
    response = client.get('/users/999999')
    print('response = client.get("/users/999999")')

    # Expecting HTTP 404 Not Found
    assert response.status_code == 404
    print('✅ Correctly failed with 404 Not Found')

# Test case 5: Upsert a user (create if not exists or update)
def test_upsert_user(client):
    print('🔄 test_upsert_user: Sending PUT to upsert user...')

    # Use a specific ID for testing upsert behavior
    user_id = '999'
    print('user_id = "999"')

    # Send a PUT request to either update or create the user
    response = client.put(f'/users/{user_id}', json={'name': 'Upserted'})
    print(f'response = client.put("/users/{user_id}", json={{"name": "Upserted"}})')

    # Expecting HTTP 200 OK (update) or 201 Created (new)
    assert response.status_code in [200, 201]
    print(f'✅ Upsert success with status: {response.status_code}')

    # Confirm the user was created/updated with the expected name
    assert response.get_json()['user']['name'] == 'Upserted'
    print('✅ Upserted user has name:', response.get_json()['user']['name'])
