import requests

# Tests if the app is running.
def test_health_check(url="http://localhost:5000"):
    response = requests.get(url)
    assert response.content == b"This a health check. Customer Management Service is up and running."