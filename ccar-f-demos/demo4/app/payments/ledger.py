"""Settlement ledger for processed payments."""

SETTLEMENTS = []


def record_settlement(payment_id, gateway, amount):
    """Record that a payment settled."""
    settlement = {
        "payment_id": payment_id,
        "gateway": gateway,
        "amount": amount,
    }
    SETTLEMENTS.append(settlement)
    return settlement


def settled_total(gateway):
    """Total settled through one gateway."""
    total = 0.0
    for settlement in SETTLEMENTS:
        if settlement["gateway"] == gateway:
            total += settlement["amount"]
    return round(total, 2)


def clear():
    SETTLEMENTS.clear()
