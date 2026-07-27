# Demo 4 — Path-scoped rules with `.claude/rules/`

No notebook for this one. This demo runs inside Claude Code in VS Code, on this
repo. You don't need the Python virtual environment or an API key — nothing here
is executed.

## What this demo shows

A rules file that only loads when Claude touches files matching a glob.

Project memory is usually all-or-nothing: a `CLAUDE.md` at the repo root applies
to everything you do. Nested `CLAUDE.md` files narrow that to a directory. But
directories are a blunt instrument — sometimes the files that need a rule are
scattered across several directories, sitting right next to files that must
*not* get it.

`.claude/rules/` solves that. Each rule file carries a `paths:` list of globs in
its YAML frontmatter, and Claude loads it only when it reads a file that matches.

## Files

The rule itself lives at the **repo root**, not in this folder — rules are
project-scoped by design and Claude only looks in `<project root>/.claude/rules/`:

```
.claude/rules/ledger-rules.md      ← the rule, scoped by a paths: glob
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

The glob is:

```yaml
---
paths:
  - "ccar-f-demos/demo4/app/**/ledger.py"
---
```

Globs are relative to the **project root**, not to the rule file. `**` matches
any depth of subdirectory.

Look at what that selects: the same filename in two different directories, while
skipping the file sitting right beside it. **That is the whole point of the
layout.** A `CLAUDE.md` in `app/billing/` would also capture `invoices.py`. One
in `app/` would capture all five files. There is no place to put a `CLAUDE.md`
that produces this selection. A glob can.

The rule body demands two things Claude would never do on its own:

- announce `Applying ledger rule LR-7.` before editing
- put a `# [LR-7]` comment above every function it writes

plus `Decimal` instead of `float`. The announcement is your live signal; the
marker is your permanent one, sitting in the diff after the stream ends.

The five source files are deliberately plain — floats everywhere, no `Decimal`,
no `# [LR-7]` markers, no house style to copy. That matters. If `ledger.py`
already demonstrated the convention, Claude could imitate the local style and the
demo would prove nothing. The rule file is the only possible source of the
marker.

## Run it

**1.** Start clean with `/clear`. Path-scoped rules load when Claude reads a
matching file, so you want a fresh context to watch it happen.

**2.** Show the audience the tree above and the contents of
`.claude/rules/ledger-rules.md`.

**3.** Ask for the same change in one covered file and one uncovered file, in a
single prompt:

> In `ccar-f-demos/demo4/app/billing/ledger.py` and
> `ccar-f-demos/demo4/app/payments/gateway.py`, add a function that applies a
> percentage discount to an amount.

**4.** Ask why they differ:

> Why did those two edits follow different conventions?

**5.** Run the negative control — the sibling in the *same directory* as a
covered file:

> Add the same discount function to `ccar-f-demos/demo4/app/billing/invoices.py`.

## What to look for

In step 3, one prompt produces two visibly different edits:

| | `billing/ledger.py` | `payments/gateway.py` |
|---|---|---|
| Announcement | `Applying ledger rule LR-7.` | none |
| Marker comment | `# [LR-7]` above the function | none |
| Money type | `Decimal` | plain `float` |
| Rounding | `.quantize(...)` | `round()` |

In step 4 Claude should name the rule file and its glob.

In step 5 `invoices.py` comes out unguarded — plain floats, no marker — despite
living in the same directory as a covered file. This is the nested-`CLAUDE.md`
argument made concrete: directory-based memory could not have produced this.

## Reset

```bash
git checkout -- ccar-f-demos/demo4/app
```

Run this between takes. The demo only works from the clean, float-based starting
state.

## Notes

- **Any filename works.** Files in `.claude/rules/` don't need to be called
  `CLAUDE.md` — name them for what they do (`ledger-rules.md`, `testing.md`,
  `security.md`) and use subdirectories if you want. Only the location matters.
- **Three mechanisms, three trigger points.** Root `CLAUDE.md` loads at session
  start and applies to everything. `@path` imports inside a `CLAUDE.md` are
  expanded at session start too — they're inlined, not conditional. Nested
  `CLAUDE.md` loads when Claude reads files in that directory. `.claude/rules/`
  with `paths:` loads only on a glob match. Know which is which.
- **Rules trigger on file reads,** not on every tool call. If Claude never opens
  a matching file, the rule never enters context — which is the point: you're
  buying back context window.
- **Brace expansion works** in the globs: `src/**/*.{ts,tsx}`.
- This rule is live for anyone working in this repo, including you. Edit either
  `ledger.py` for any reason and LR-7 applies.
