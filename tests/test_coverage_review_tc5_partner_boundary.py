from src.coverage_review_tc5_partner_boundary import resolve_partner_value

def test_internal_value_is_preserved():
    assert resolve_partner_value({"certificate_id": 0}) == 0

def test_absent_value_uses_default():
    assert resolve_partner_value({}) == ""
