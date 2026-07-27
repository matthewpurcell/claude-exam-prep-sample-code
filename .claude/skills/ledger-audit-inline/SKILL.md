---
name: ledger-audit-inline
description: Same audit as ledger-audit, but runs in the main conversation instead of a forked context. Exists purely as the control arm of demo 5.
argument-hint: [path-to-audit]
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, Write, Bash
---

# Ledger audit

Audit the Python files under the path given in `$ARGUMENTS`. If no path was
supplied, audit `ccar-f-demos/demo4/app`.

Look for money being handled as `float` rather than `decimal.Decimal`:

- `0.0` or other float literals used as a running monetary total
- arithmetic on `amount` fields without `Decimal`
- the built-in `round()` used to fix currency to two places
- percentages written as float literals

## Report

Output a markdown table with one row per offending file: **File**, **Line**,
**What's wrong**. Sort the worst offenders first. Do not fix anything — just
report.

Then, on a final line, answer this question plainly:

> Can you see any earlier conversation from this session? Quote anything the user
> asked you to remember, or say that you have no prior conversation available.
