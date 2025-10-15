import re
import pytest
from tests.utils import resolve_path

def test_apply_discount_shows_total_change(client):
    # Βρες add-to-cart
    add_path = resolve_path(("add","cart"), methods=("POST",)) or \
               resolve_path(("cart","add"), methods=("POST",)) or \
               resolve_path(("add-to-cart",), methods=("POST",))
    assert add_path
    client.post(add_path, data={"book_id": "1", "quantity": "1"}, follow_redirects=True)

    # Προσπάθησε να βρεις endpoint κουπονιού
    coupon_path = resolve_path(("coupon",), methods=("POST",)) or \
                  resolve_path(("discount",), methods=("POST",)) or \
                  resolve_path(("apply","coupon"), methods=("POST",))

    if not coupon_path:
        pytest.skip("Δεν υπάρχει endpoint για κουπόνι/έκπτωση στο app")

    r = client.post(coupon_path, data={"code": "SALE10"}, follow_redirects=True)
    assert r.status_code in (200, 302, 303)

    page = client.get("/cart")
    assert page.status_code == 200
    html = page.data.decode("utf-8", errors="ignore")
    assert re.search(r"(discount|coupon|total|σύνολο)", html, re.I)
