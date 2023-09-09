import pytest
from server import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client

def test_get_users(client):
    # Clear the database first
    User.query.delete()
    db.session.commit()

    # Add test users to the database
    user1 = User(name='John', age=30, address='123 Main St')
    user2 = User(name='Alice', age=25, address='456 Elm St')
    db.session.add_all([user1, user2])
    db.session.commit()

    response = client.get('/users')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


def test_get_user(client):
    user = User(name='John', age=30, address='123 Main St')
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/user/{user.id}')
    data = response.get_json()  # Use get_json() to parse JSON

    assert response.status_code == 200
    assert data['name'] == 'John'

def test_add_user(client):
    new_user = {
        'name': 'Alice',
        'age': 25,
        'address': '456 Elm St'
    }

    response = client.post('/user', json=new_user)
    data = response.get_json()

    if response.status_code == 201:
        assert 'id' in data
        assert data['name'] == 'Alice'
        assert data['age'] == 25
        assert data['address'] == '456 Elm St'
    elif response.status_code == 400:
        # Handle the case where the user already exists
        assert 'error' in data
        assert 'User with the same name, address, and age already exists' in data['error']
    else:
        assert False, f"Unexpected response status code: {response.status_code}"


def test_delete_user(client):
    user = User(name='John', age=30, address='123 Main St')
    db.session.add(user)
    db.session.commit()

    response = client.delete(f'/user/{user.id}')

    assert response.status_code == 200
    assert response.get_json()['name'] == 'John'

def test_increment_point(client):
    user = User(name='John', age=30, address='123 Main St')
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/user/{user.id}/increment')
    data = response.get_json()  # Use get_json() to parse JSON

    assert response.status_code == 200
    assert data['points'] == 1

def test_decrement_point(client):
    user = User(name='John', age=30, address='123 Main St', points=1)
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/user/{user.id}/decrement')
    data = response.get_json()  # Use get_json() to parse JSON

    assert response.status_code == 200
    assert data['points'] == 0

def test_decrement_point_zero(client):
    user = User(name='John', age=30, address='123 Main St', points=0)
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/user/{user.id}/decrement')

    assert response.status_code == 400
    assert 'Score already 0' in response.get_json()['error']

def test_duplicate_user(client):
    existing_user = {
        'name': 'John',
        'age': 30,
        'address': '123 Main St'
    }

    # Add an existing user to the database
    existing_user_record = User(**existing_user)
    db.session.add(existing_user_record)
    db.session.commit()

    response = client.post('/user', json=existing_user)

    assert response.status_code == 400
    assert 'User with the same name, address, and age already exists' in response.get_json()['error']

def test_invalid_inputs_when_creating_user(client):
    invalid_user = {
        'name': '',
        'age': -5,  # Invalid age
        'address': '456 Elm St'
    }

    response = client.post('/user', json=invalid_user)

    assert response.status_code == 400
    assert 'Name and Address fields are required' in response.get_json()['error']