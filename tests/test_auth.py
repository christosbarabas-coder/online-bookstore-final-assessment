def test_login_page_loads(client):
    r = client.get("/login")
    assert r.status_code == 200

# Αν έχεις demo credentials στο README (π.χ. demo@bookstore.com / demo123),
# ξεκλείδωσε το παρακάτω και άλλαξε τα στοιχεία αν χρειάζεται.
# def test_login_attempt(client):
#     r = client.post("/login", data={"email":"demo@bookstore.com","password":"demo123"}, follow_redirects=True)
#     assert r.status_code in (200, 302)
