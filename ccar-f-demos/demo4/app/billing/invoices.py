"""Invoice rendering."""


def invoice_total(line_items):
    """Sum the line items on an invoice."""
    total = 0.0
    for item in line_items:
        total += item["amount"] * item["quantity"]
    return round(total, 2)


def format_invoice(customer, line_items):
    """Render a plain-text invoice."""
    lines = [f"Invoice for {customer}", "-" * 32]
    for item in line_items:
        lines.append(f"{item['description']:<20} {item['amount']:>8.2f}")
    lines.append("-" * 32)
    lines.append(f"{'Total':<20} {invoice_total(line_items):>8.2f}")
    return "\n".join(lines)
