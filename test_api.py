import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_add_and_get_word(client):
    res = client.post('/api/words', json={'word': 'hello'})
    assert res.status_code == 201

    res = client.get('/api/words/hello')
    assert res.status_code == 200
    assert res.get_json()['word'] == 'hello'

def test_duplicate_word(client):
    client.post('/api/words', json={'word': 'duplicate'})
    res = client.post('/api/words', json={'word': 'duplicate'})
    assert res.status_code == 400

def test_update_word(client):
    client.post('/api/words', json={'word': 'old'})
    res = client.put('/api/words/old', json={'word': 'new'})
    assert res.status_code == 200
    res = client.get('/api/words/new')
    assert res.status_code == 200

def test_delete_word(client):
    client.post('/api/words', json={'word': 'delete'})
    res = client.delete('/api/words/delete')
    assert res.status_code == 200
    res = client.get('/api/words/delete')
    assert res.status_code == 404
