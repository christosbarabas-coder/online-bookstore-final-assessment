from tests.utils import resolve_path

def test_add_to_cart_and_checkout_flow(client):
    # cart page πρέπει να φορτώνει
    r = client.get("/cart")
    assert r.status_code in (200, 302)

    # Βρες endpoint για προσθήκη στο καλάθι (π.χ. "/add-to-cart")
    add_path = resolve_path(("add","cart"), methods=("POST",)) or \
               resolve_path(("cart","add"), methods=("POST",)) or \
               resolve_path(("add-to-cart",), methods=("POST",))
    assert add_path, "Δεν βρέθηκε endpoint για προσθήκη στο cart"
    r = client.post(add_path, data={"book_id": "1", "quantity": "1"}, follow_redirects=True)
    assert r.status_code in (200, 302, 303)

    # checkout route (GET)
    r = client.get("/checkout")
    assert r.status_code in (200, 302)
