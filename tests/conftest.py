import sys, os
# Κάνε import το app.py από το root του repo όταν τρέχει το CI
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app

@pytest.fixture
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as c:
        with app.app_context():
            yield c
