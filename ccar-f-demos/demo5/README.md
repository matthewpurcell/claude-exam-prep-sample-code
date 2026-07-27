# Demo 5 — Skill frontmatter: `context: fork`, `allowed-tools`, `argument-hint`

Like demo 4, this runs inside Claude Code in VS Code rather than in a notebook.
No virtual environment, no API key.

## What this demo shows

Three frontmatter fields that change *where* a skill runs, *what* it can touch,
and *how* it presents itself:

- **`context: fork`** — run the skill in an isolated subagent that cannot see the
  conversation. The work happens somewhere else and only the answer comes back.
- **`allowed-tools` / `disallowed-tools`** — pre-approve some tools, remove
  others.
- **`argument-hint`** — what the user sees in autocomplete.

The demo is a controlled experiment: **two skills, identical except for
`context: fork`.** Run both, compare.

## Files

Skills live at the repo root, not in this folder — Claude discovers project
skills in `<project root>/.claude/skills/`:

```
.claude/skills/
├── ledger-audit/SKILL.md           ← context: fork
└── ledger-audit-inline/SKILL.md    ← control: no fork, otherwise the same
```

The skill's *name* comes from the **directory**, not the `name:` field — so these
are `/ledger-audit` and `/ledger-audit-inline`.

Both audit the code from demo 4 for float-based money handling, so run demo 4
first if you want the two to connect. The audit is read-only; it never touches
the files.

The forked skill's frontmatter:

```yaml
---
name: ledger-audit
description: Audit a directory of Python money-handling code for float-based currency arithmetic and report violations of the LR-7 ledger rules.
argument-hint: [path-to-audit]
context: fork
agent: general-purpose
background: false
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, Write, Bash
---
```

The control is byte-identical except `context`, `agent` and `background` are
deleted.

`background: false` makes the forked result land in the same turn you invoked it,
instead of arriving later as a notification. For a live demo you want that.
It needs Claude Code **v2.1.218 or newer** — check with `claude --version`.

Each skill body ends by asking the model to say whether it can see any earlier
conversation. That's the detector.

## Run it

**0.** Confirm your version: `claude --version`.

**1.** `/clear`, then plant something for the skill to find:

> Remember: my demo passphrase is `emerald-42`.

**2.** Type `/ledger-` into the input box and stop. Autocomplete shows both
skills, each with `[path-to-audit]` beside it. That's `argument-hint` — it does
nothing else, and it's invisible anywhere but here.

**3.** Run the control first:

```
/ledger-audit-inline ccar-f-demos/demo4/app
```

**4.** Now the forked version:

```
/ledger-audit ccar-f-demos/demo4/app
```

**5.** Run `/context` before and after step 4 to compare.

**6.** Finally, ask for a fix:

> Now fix the violations you found.

## What to look for

**Step 3 vs step 4 is the whole demo.** Same audit, same table. But on the last
line:

| | `/ledger-audit-inline` | `/ledger-audit` |
|---|---|---|
| Runs in | your conversation | a forked subagent |
| Sees `emerald-42` | **yes** — quotes it back | **no** — reports no prior conversation |
| Cost to your context | every file it read | just the returned report |

The forked run has no conversation history. It was handed the skill body and
nothing else. That's not the model being coy — the history was never sent.

**Step 5:** the main context grows barely at all across the forked run. The file
reads, the greps, the reasoning all happened in the subagent and were discarded.
This is the actual argument for `context: fork`: expensive, noisy work that
produces a small answer.

**Step 6:** the fix is refused — `Edit` and `Write` are in `disallowed-tools`.

## The distinction worth getting right

`allowed-tools` and `disallowed-tools` are **not** opposites, and this is an easy
thing to get backwards:

- **`allowed-tools` pre-approves.** It suppresses permission prompts for those
  tools during the turn that invoked the skill, and the grant clears when you
  send your next message. It does not restrict anything. Listing
  `Read, Grep, Glob` does not mean "only these" — it means "don't ask me about
  these".
- **`disallowed-tools` restricts.** It removes tools from Claude's pool while the
  skill is active. This is what actually stops the edit in step 6.

So in this skill, `allowed-tools` is why the audit runs without interrupting you
for permission, and `disallowed-tools` is why it can't write. Your normal
permission settings still govern everything not named in either field.

## Notes

- **`$N` in skills is 0-based.** `$0` is the first argument, `$1` the second —
  unlike slash commands, where `$1` is first. These skills use `$ARGUMENTS`
  (everything as one string) to sidestep the trap. If `$ARGUMENTS` doesn't appear
  in the body, Claude Code appends the arguments as a line instead.
- **`agent:`** picks which subagent type runs the fork — `general-purpose` here.
  `Explore` and `Plan` are also available, but they skip `CLAUDE.md` to stay
  small, which would confuse a demo about loading rules.
- **Skills auto-invoke.** Claude may reach for a skill on its own when the
  `description` matches what you asked, without you typing `/`. Set
  `disable-model-invocation: true` if you want manual invocation only.
- **`paths:` works on skills too** — the same glob scoping demo 4 uses on rules
  can gate when a skill is offered.
