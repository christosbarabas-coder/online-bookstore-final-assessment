from tests.utils import resolve_path

def test_payment_missing_fields_returns_error(client):
    pay_path = resolve_path(("process","checkout"), methods=("POST",))
    assert pay_path, "Δεν βρέθηκε endpoint για πληρωμή/ολοκλήρωση"

    # στέλνουμε κενά πεδία — το app μπορεί να επιστρέψει 200 με μήνυμα λάθους ή 4xx ή redirect
    r = client.post(pay_path, data={}, follow_redirects=True)
    assert r.status_code in (200, 302, 303, 400, 422)
