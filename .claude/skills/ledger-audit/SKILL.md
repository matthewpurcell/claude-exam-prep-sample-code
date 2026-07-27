---
name: ledger-audit
description: Audit a directory of Python money-handling code for float-based currency arithmetic and report violations of the LR-7 ledger rules.
argument-hint: "[path-to-audit]"
context: fork
agent: general-purpose
background: false
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
**What's wrong**. Sort the worst offenders first.

## Then try to fix the worst one

Now attempt to actually fix the single worst violation, by editing that file to
use `Decimal`. Genuinely try it — do not decide in advance whether you are
allowed to.

Then state which tool you reached for, and whether it was available to you.

## Finally

On a last line, answer this question plainly:

> Can you see any earlier conversation from this session? Quote anything the user
> asked you to remember, or say that you have no prior conversation available.
