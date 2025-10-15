from app import app

def resolve_path(keywords, methods=("POST",)):
    """
    Βρες route που να περιέχει ΟΛΕΣ τις λέξεις-κλειδιά (με σειρά αδιάφορη)
    και να υποστηρίζει τις ζητούμενες μεθόδους (default: POST).
    Επιστρέφει το rule string (π.χ. "/cart/add") ή None.
    """
    keys = tuple(k.lower() for k in keywords)
    need = set(methods)
    for rule in app.url_map.iter_rules():
        rule_methods = {m for m in rule.methods if m not in ("HEAD", "OPTIONS")}
        if not need.issubset(rule_methods):
            continue
        rule_str = str(rule.rule).lower()
        if all(k in rule_str for k in keys):
            return str(rule.rule)
    return None
