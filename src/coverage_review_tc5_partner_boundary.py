def resolve_partner_value(payload, default=""):
    value = payload.get("certificate_id")
    if value is None:
        value = payload.get("certificateId")
    return default if value in (None, "") else value
