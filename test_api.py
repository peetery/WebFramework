import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_api_get_data(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    assert response.json == []

    for i in range(3):
        response = client.post('/api/data', json={
            'feature1': 1.0 + i,
            'feature2': 2.0 + i,
            'category': i + 1
        })
        assert response.status_code == 201

    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 3


def test_api_post_data(client):
    data = {'feature1': 1.23, 'feature2': 4.56, 'category': 2}
    response = client.post('/api/data', json=data)
    assert response.status_code == 201
    assert 'id' in response.json

    response = client.get('/api/data')
    data = response.json[0]
    assert data['feature1'] == 1.23
    assert data['feature2'] == 4.56
    assert data['category'] == 2

    invalid_data = {'feature1': 1.23, 'feature2': 4.56}
    response = client.post('/api/data', json=invalid_data)
    assert response.status_code == 400
    assert 'error' in response.json


def test_api_delete_data(client):
    response = client.post('/api/data', json={
        'feature1': 1.23,
        'feature2': 4.56,
        'category': 2
    })
    assert response.status_code == 201
    record_id = response.json['id']

    response = client.delete(f'/api/data/{record_id}')
    assert response.status_code == 200
    assert response.json['id'] == record_id

    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.json
    assert all(record['id'] != record_id for record in data)

    response = client.delete('/api/data/9999')
    assert response.status_code == 404
    assert 'error' in response.json
