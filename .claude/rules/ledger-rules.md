---
paths:
  - "ccar-f-demos/demo4/app/**/ledger.py"
---

# Ledger rules (LR-7)

These rules govern the ledger modules only. They are not house style for the rest
of the codebase.

Before you edit a file governed by this rule, state exactly this line:

`Applying ledger rule LR-7.`

Then apply all of the following:

- Monetary amounts use `decimal.Decimal`. Never `float`.
- Immediately precede every function you add or modify with a `# [LR-7]` comment
  line, on its own line above the `def`.
- Round explicitly, never with the built-in `round()`:
  `.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`
- Percentages are `Decimal` too — write `Decimal("0.10")`, not `0.10`.
