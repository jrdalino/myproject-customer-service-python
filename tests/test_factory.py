import pytest
from flaskr import create_app

# You must create a mock app
@pytest.fixture
def app():
	app = create_app()
	return app

# @pytest.fixture
def test_health_check(client):
    response = client.get("/")
    assert response.data == b"This a health check. Customer Management Service is up and running."
