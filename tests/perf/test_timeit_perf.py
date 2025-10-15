import timeit
from app import app

def test_homepage_under_100ms():
    with app.test_client() as c:
        t = timeit.timeit(lambda: c.get("/"), number=5)
        # μέσος χρόνος ~ t/5. Θέτουμε χαλαρό όριο 0.5s σύνολο για 5 hits (=100ms/req)
        assert t < 0.5, f"Homepage too slow: {t:.3f}s for 5 requests"
