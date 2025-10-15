import pytest

@pytest.mark.parametrize("path", ["/", "/cart", "/checkout", "/login"])
def test_smoke_routes(client, path):
    r = client.get(path)
    assert r.status_code in (200, 302)
