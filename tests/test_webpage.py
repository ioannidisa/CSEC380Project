import requests


def test_has_hello_world():
    response = requests.get('http://localhost:8080/')
    body = response.text
    assert 'Hello World' in body
