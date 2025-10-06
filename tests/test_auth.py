from app.models import User


def test_user_registration(client):
    # preparing json registration request
    response = client.post("/api/auth/register", json={
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


def test_invalid_registration(client):
    # preparing json invalid registration request without username
    response1 = client.post("/api/auth/register", json={
        "email": "test@emial.com",
        "password": "test"
    })
    assert response1.status_code == 400

    # preparing json invalid registration request without email
    response1 = client.post("/api/auth/register", json={
        "username": "test_user",
        "password": "test"
    })
    assert response1.status_code == 400

    # preparing json invalid registration request without password
    response1 = client.post("/api/auth/register", json={
        "username": "test_user",
        "email": "test@emial.com"
    })
    assert response1.status_code == 400

    # checking that no user was added to database
    assert User.query.count() == 0


def test_duplicate_registration(client):
    # first registration
    response1 = client.post("/api/auth/register", json={
        "username": "duplicate",
        "email": "duplicate@emial.com",
        "password": "duplicate"
    })
    assert response1.status_code == 200
    assert User.query.count() == 1

    # same username check
    response2 = client.post("/api/auth/register", json={
        "username": "duplicate",
        "email": "non-duplicate@emial.com",
        "password": "duplicate"
    })
    assert response2.status_code == 401
    assert User.query.count() == 1

    # same email check
    response3 = client.post("/api/auth/register", json={
        "username": "non-duplicate",
        "email": "duplicate@emial.com",
        "password": "duplicate"
    })
    assert response3.status_code == 401
    assert User.query.count() == 1


def test_login(client):
    # registring new user
    response1 = client.post("/api/auth/register", json={
        "username": "test_user",
        "email": "test@emial.com",
        "password": "test"
    })

    # checking if status is okay and user was added to the query
    assert response1.status_code == 200
    assert User.query.count() == 1

    # loggin in new user
    response2 = client.post("/api/auth/login", json={
        "email": "test@emial.com",
        "password": "test"
    })

    # checking if status is okay
    assert response2.status_code == 200

    # checking if backend returned jwt
    data = response2.get_json()
    assert 'access_token' in data and isinstance(data['access_token'], str)
    
