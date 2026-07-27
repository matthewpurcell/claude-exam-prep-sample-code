"""Line-item ledger for customer billing."""

ENTRIES = []


def post_line_item(account_id, description, amount):
    """Record a charge against an account."""
    entry = {
        "account_id": account_id,
        "description": description,
        "amount": amount,
    }
    ENTRIES.append(entry)
    return entry


def account_balance(account_id):
    """Total everything posted against one account."""
    total = 0.0
    for entry in ENTRIES:
        if entry["account_id"] == account_id:
            total += entry["amount"]
    return round(total, 2)


def clear():
    ENTRIES.clear()
