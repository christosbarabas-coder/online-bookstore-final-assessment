import pytest
from app import app

@pytest.fixture
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as c:
        with app.app_context():
            yield c
