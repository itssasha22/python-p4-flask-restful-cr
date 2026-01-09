
import pytest
from server.app import app, db
from server.models import Newsletter

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Welcome to the Newsletter RESTful API"

def test_get_newsletters_empty(client):
    response = client.get('/newsletters')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_post_newsletter(client):
    response = client.post('/newsletters', data={'title': 'Test Title', 'body': 'Test Body'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Title'
    assert data['body'] == 'Test Body'
    assert 'id' in data
    assert 'published_at' in data

def test_get_newsletters_after_post(client):
    client.post('/newsletters', data={'title': 'Test Title', 'body': 'Test Body'})
    response = client.get('/newsletters')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Title'

def test_get_newsletter_by_id(client):
    post_response = client.post('/newsletters', data={'title': 'Test Title', 'body': 'Test Body'})
    newsletter_id = post_response.get_json()['id']
    response = client.get(f'/newsletters/{newsletter_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Title'
    assert data['body'] == 'Test Body'

def test_get_newsletter_by_invalid_id(client):
    response = client.get('/newsletters/999')
    assert response.status_code == 404  # Assuming it raises 404, but in code it's not handled, wait.

# Note: The current code doesn't handle 404 for invalid ID, it will raise AttributeError if not found.
# For thorough testing, we should add error handling in the code.
