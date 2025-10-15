# tests/conftest.py
import sys
from pathlib import Path
import pytest

# Πρόσθεσε το root του project στο sys.path ώστε να βρίσκει το app.py στο CI
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app

@pytest.fixture
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as c:
        with app.app_context():
            yield c
