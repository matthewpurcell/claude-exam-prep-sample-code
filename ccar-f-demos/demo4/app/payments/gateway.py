"""Stub payment gateway client. Nothing here talks to a real network."""

CHARGES = {}


def charge(card_token, amount, currency="AUD"):
    """Pretend to charge a card and hand back a receipt."""
    payment_id = f"pay_{len(CHARGES) + 1:04d}"
    CHARGES[payment_id] = {
        "card_token": card_token,
        "amount": amount,
        "currency": currency,
        "status": "captured",
    }
    return payment_id


def refund(payment_id, amount):
    """Reverse part or all of a charge."""
    charge_record = CHARGES.get(payment_id)
    if charge_record is None:
        raise KeyError(payment_id)
    charge_record["amount"] = round(charge_record["amount"] - amount, 2)
    if charge_record["amount"] <= 0:
        charge_record["status"] = "refunded"
    return charge_record
