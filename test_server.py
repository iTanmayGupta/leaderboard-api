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
    user1 = User(name='Popp', age=30, address='Germany')
    user2 = User(name='Grace', age=25, address='Peru')
    db.session.add_all([user1, user2])
    db.session.commit()

    response = client.get('/users')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


def test_get_user(client):
    user = User(name='Tanmay', age=23, address='Toronto')
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/user/{user.id}')
    data = response.get_json()  # Use get_json() to parse JSON

    assert response.status_code == 200
    assert data['name'] == 'Tanmay'

def test_add_user(client):
    new_user = {
        'name': 'Alcaraz',
        'age': 20,
        'address': 'Spain'
    }

    response = client.post('/user', json=new_user)
    data = response.get_json()

    if response.status_code == 201:
        assert 'id' in data
        assert data['name'] == 'Alcaraz'
        assert data['age'] == 20
        assert data['address'] == 'Spain'
    elif response.status_code == 400:
        # Handle the case where the user already exists
        assert 'error' in data
        assert 'User with the same name, address, and age already exists' in data['error']
    else:
        assert False, f"Unexpected response status code: {response.status_code}"


def test_delete_user(client):
    user = User(name='Kroos', age=34, address='Germany')
    db.session.add(user)
    db.session.commit()

    response = client.delete(f'/user/{user.id}')

    assert response.status_code == 200
    assert response.get_json()['name'] == 'Kroos'

def test_increment_point(client):
    user = User(name='Hamilton', age=37, address='UK')
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/user/{user.id}/increment')
    data = response.get_json()  # Use get_json() to parse JSON

    assert response.status_code == 200
    assert data['points'] == 1

def test_decrement_point(client):
    user = User(name='Woods', age=43, address='Nigeria', points=1)
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/user/{user.id}/decrement')
    data = response.get_json()  # Use get_json() to parse JSON

    assert response.status_code == 200
    assert data['points'] == 0

def test_decrement_point_zero(client):
    user = User(name='Kohli', age=35, address='Delhi', points=0)
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/user/{user.id}/decrement')

    assert response.status_code == 400
    assert 'Score already 0' in response.get_json()['error']

def test_duplicate_user(client):
    existing_user = {
        'name': 'Kvara',
        'age': 24,
        'address': 'Georgia'
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
        'address': 'USA'
    }

    response = client.post('/user', json=invalid_user)

    assert response.status_code == 400
    assert 'Name and Address fields are required' in response.get_json()['error']