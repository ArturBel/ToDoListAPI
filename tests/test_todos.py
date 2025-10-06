from app.models import User, Todo
from flask_jwt_extended import get_jwt_identity


# function to register user and get his jwt
def register_user(client):
    # preparing json registration request
    response = client.post('/api/auth/register', json={
        "username": "test_user",
        "email": "test@emial.com",
        "password": "test"
    })

    # checking if status is okay and user was added to the query
    assert response.status_code == 200
    assert User.query.count() == 1

    # checking if backed hashed user's password
    new_user = User.query.first()
    assert new_user.password_hash != "test"

    # checking if backend returned jwt
    data = response.get_json()
    assert 'access_token' in data and isinstance(data['access_token'], str)

    # returning jwt token for other tests
    return response.get_json()['access_token']


def test_crud(client):
    # getting user's token and preparing headers
    access_token = register_user(client=client)
    headers = {'Authorization': f'Bearer {access_token}'}

    # checking that no todos are present for new user
    empty_get_response = client.get("/api/todos/", headers=headers)
    assert empty_get_response.get_json() == {"msg": "nothing to display"}

    # invalid create response
    invalid_create_response = client.post('/api/todos/', json={
        "description": "Title is required, unlike description",
        "invalid": "This should not be saved"
    }, headers=headers)

    # checking if invalid todo is not saved
    assert invalid_create_response.status_code == 500
    assert Todo.query.count() == 0

    # valid create
    create_response = client.post('/api/todos/', json={
        "title": "Test crud",
        "description": "Check if crud functions work correctly"
    }, headers=headers)

    # checking if todo is saved
    assert create_response.status_code == 201
    assert Todo.query.count() == 1

    # checking if todo has all required fields and all of them are correct
    data = create_response.get_json()
    assert 'id' in data and isinstance(data['id'], int)
    assert 'title' in data and isinstance(data['title'], str) and data['title'] == 'Test crud'
    assert 'description' in data and isinstance(data['description'], str) and data['description'] == "Check if crud functions work correctly"
    assert 'completed' in data and isinstance(data['completed'], bool) and data['completed'] == False
    assert 'created_at' in data and isinstance(data['created_at'], str)
    assert 'updated_at' in data and isinstance(data['updated_at'], str)
    assert 'owner_id' in data and isinstance(data['owner_id'], int) and data['owner_id'] == int(get_jwt_identity())
    assert 'owner' in data and isinstance(data['owner'], dict)

    # checking update function
    update_response = client.put(f'/api/todos/{data['id']}', json={'completed': True}, headers=headers)
    #updated = update_response.get_json()
    updated = client.get(f'/api/todos/{data['id']}', headers=headers).get_json()
    assert update_response.status_code == 200
    assert updated['completed'] == True

    # checking delete function
    client.delete(f'/api/todos/{updated['id']}', headers=headers)
    assert Todo.query.count() == 0
