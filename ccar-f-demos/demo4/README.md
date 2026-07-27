# Demo 4 — Path-scoped rules with `.claude/rules/`

This demo runs inside Claude Code in VS Code on this repo. You do not need a Python virtual environment or an API key — nothing
is executed.

## What this demo shows

A rules file that only loads when Claude touches files matching a glob.

Project memory is usually all-or-nothing: a `CLAUDE.md` at the repo root applies to everything. Nested `CLAUDE.md` files narrow that to a directory. But directories are a blunt instrument — sometimes the files that need a rule are scattered across several directories, sitting next to files that must *not* have the rule applied.

Using `.claude/rules/` addresses this limitation. Each rule file carries a `paths:` list of globs in its YAML frontmatter and Claude loads it only when it reads a file that matches.

## Files

Rules live in `<project root>/.claude/rules/`. For our demo, we have one rule:

```
.claude/rules/ledger-rules.md
```

The code it governs lives here:

```
ccar-f-demos/demo4/app/
├── billing/
│   ├── ledger.py        ← COVERED by the glob
│   └── invoices.py      ← sibling, NOT covered
├── payments/
│   ├── ledger.py        ← COVERED by the glob
│   └── gateway.py       ← sibling, NOT covered
└── reporting/
    └── summary.py       ← NOT covered
```

The `.claude/rules/ledger-rules.md` rule file has this glob at the top which scopes it to specific files:

```yaml
---
paths:
  - "ccar-f-demos/demo4/app/**/ledger.py"
---
```

Globs are relative to the **project root** not to the rule file. `**` matches
any depth of subdirectory.

This rule will select the same filename in two different directories, while skipping the file sitting right beside it. **That is the whole point of rule files.** A `CLAUDE.md` in `app/billing/` would also capture `invoices.py`. One in `app/` would capture all five files. There is no place to put a `CLAUDE.md` that results this selection wheras a glob can.

The body of our rule demands two things Claude would never do on its own:

- announce `Applying ledger rule LR-7.` before editing
- put a `# [LR-7]` comment above every function it writes
- write `Decimal` data types instead of `float`.

Note that the announcement is a live signal which will be output by Claude Code so we know the rule is being used, and the marker is a permanent comment in the edited files.

The five source files are deliberately plain — floats everywhere, no `Decimal`, no `# [LR-7]` markers, no house style to copy. This is intentional for this demo because if the source files already demonstrated the convention, Claude could imitate the local style and the demo would prove nothing. The rule file is the only possible source of the style and behaviour requirements.

## Run it

**1.** Start clean with `/clear`. Path-scoped rules load when Claude reads a matching file, so you want a fresh context to watch it happen.

**2.** Inspect the contents of
`.claude/rules/ledger-rules.md`.

**3.** Ask Claude Code for the same change in one covered file and one uncovered file, in a single prompt:

```
In `ccar-f-demos/demo4/app/billing/ledger.py` and `ccar-f-demos/demo4/app/payments/gateway.py` add a function that applies a percentage discount to an amount.
```

**4.** Ask why they differ:

```
Why did those two edits follow different conventions?
```

**5.** Run the negative control — the sibling in the *same directory* as a covered file:

```
Add the same discount function to `ccar-f-demos/demo4/app/billing/invoices.py`.
```

## Reset

```bash
git checkout -- ccar-f-demos/demo4/app
```