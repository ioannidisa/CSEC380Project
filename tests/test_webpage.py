import requests


def test_has_hello_world():
    response = requests.get('http://localhost:8080/')
    assert 'Hello World' in response.text