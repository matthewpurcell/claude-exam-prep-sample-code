"""Period roll-ups for the finance team."""


def period_total(records, start, end):
    """Total the records that fall inside a date range."""
    total = 0.0
    for record in records:
        if start <= record["date"] <= end:
            total += record["amount"]
    return round(total, 2)


def average_transaction(records):
    """Mean transaction size across the supplied records."""
    if not records:
        return 0.0
    return round(sum(r["amount"] for r in records) / len(records), 2)


def top_accounts(records, limit=5):
    """Rank accounts by spend, highest first."""
    totals = {}
    for record in records:
        totals[record["account_id"]] = totals.get(record["account_id"], 0.0) + record["amount"]
    ranked = sorted(totals.items(), key=lambda pair: pair[1], reverse=True)
    return ranked[:limit]
