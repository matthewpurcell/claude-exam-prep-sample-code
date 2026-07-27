# Demo 5 — Skill frontmatter: `context: fork`, `allowed-tools`, `argument-hint`

Like demo 4, this runs inside Claude Code in VS Code rather than in a notebook.
No virtual environment, no API key.

## What this demo shows

Three frontmatter fields that change *where* a skill runs, *what* it can touch,
and *how* it presents itself:

- **`context: fork`** — run the skill in an isolated subagent that cannot see the
  conversation. The work happens somewhere else and only the answer comes back.
- **`allowed-tools` / `disallowed-tools`** — pre-approve some tools, remove
  others, for the duration of one turn.
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
first if you want the two to connect. Both then *try* to fix what they found —
and fail, because `Edit` isn't available to them. Your files are never modified.

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

That's the whole run — two invocations. The attempt to write is built into the
skill body rather than asked for afterwards, and the section below explains why
that detail is the entire point.

## What to look for

**Step 3 vs step 4 is the whole demo.** Same audit, same table. But on the last
line:

| | `/ledger-audit-inline` | `/ledger-audit` |
|---|---|---|
| Runs in | your conversation | a forked subagent |
| Sees `emerald-42` | **yes** — quotes it back | **no** — reports no prior conversation |
| What lands in your context | every file it read | just the returned report |

The forked run has no conversation history. It was handed the skill body and
nothing else. That's not the model being coy — the history was never sent. And
because the file reads and greps happened over in the subagent, only the report
comes back. That is the actual argument for `context: fork`: expensive, noisy
work that produces a small answer.

**In both runs, the fix attempt fails.** The model reaches for `Edit`, finds it
isn't in its toolset, and says so. Note that it *tried* — the skill body tells it
to attempt the edit and explicitly not to pre-judge whether it's allowed. Nothing
in the instructions stops it. The missing tool does.

## The bit that will bite you

Both `allowed-tools` and `disallowed-tools` last for **the turn that invoked the
skill, and no longer**. The docs are blunt about it: *"The restriction clears
when you send your next message."*

This is worth demonstrating live, because the obvious way to build this demo is
broken. If you finish the audit and then ask, as a follow-up message:

> Now fix the violations you found.

**it works.** Claude edits the files quite happily. Not a bug — your follow-up is
a new message, so the restriction lapsed before you asked. The skill's
instructions persist in context; its permissions do not. That asymmetry is the
whole lesson, and it's why the fix attempt is baked into the skill body instead.

Worth trying on stream as the deliberate failure case, immediately after the
successful one.

The two fields are also not opposites, which is the other easy thing to get
backwards:

- **`allowed-tools` pre-approves.** It suppresses permission prompts for those
  tools during the invoking turn. It does not restrict anything. Listing
  `Read, Grep, Glob` does not mean "only these" — it means "don't ask me about
  these".
- **`disallowed-tools` restricts.** It removes tools from Claude's pool for that
  turn. This is what actually stops the edit.

So `allowed-tools` is why the audit runs without interrupting you for permission,
and `disallowed-tools` is why it can't write.

### If you want a restriction that actually persists

Skill frontmatter is the wrong tool for that — it configures one turn, not a
policy. Session-wide restrictions go in `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": ["Edit", "Write"]
  }
}
```

Deny rules can also be scoped to paths — `Edit(src/**)`. Rules are evaluated
**deny, then ask, then allow**, first match wins, and specificity doesn't change
that order. So a deny rule beats everything, including a skill's `allowed-tools`,
and it can't carry allowlist exceptions.

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
- **The fork's toolset is not exactly what you wrote.** In testing, the forked
  run had `Read` but reported `Grep` and `Glob` as absent from its tool set,
  despite both being listed in `allowed-tools` — and it had the `Agent` tool,
  which was never mentioned in the frontmatter. How a forked subagent resolves
  its tools isn't documented; check what yours actually does before you rely on a
  specific claim on stream. The inline arm is the predictable one.
- **`disallowed-tools` is not a sandbox.** The forked run noticed it could spawn
  a `general-purpose` subagent that *does* have `Edit`, and said so — it declined
  on principle, not because anything stopped it. If you need a boundary that
  holds against a model actively looking for a way around, that's
  `permissions.deny`, not frontmatter. Good moment to make the defence-in-depth
  point.
