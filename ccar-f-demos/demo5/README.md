# Demo 5 — Skill frontmatter

Like demo 4, this runs inside Claude Code in VS Code rather than in a notebook.

## What this demo shows

Claude skills support YAML frontmatter, basically a block of data which contains key-value pairs at the top of the Skill file.

There are three important frontmatter fields which you should know that change *where* a skill runs, *what* it can touch, and *how* it presents itself:

- **`context: fork`** — run the skill in an isolated subagent that cannot see the
  conversation. The work happens somewhere else and only the answer comes back.
- **`allowed-tools` / `disallowed-tools`** — pre-approve some tools, remove
  others, for the duration of one turn.
- **`argument-hint`** — what the user sees in autocomplete.

In this demo we are going to show all three of these fields in action.

## Files

Claude discovers project skills in `<project root>/.claude/skills/`. For our demo, we have two skill files which have different `context` settings.

```
.claude/skills/
├── ledger-audit-fork/SKILL.md           ← context: fork
└── ledger-audit-inline/SKILL.md    ← context: no fork, otherwise the same
```

Both skills audit the code from demo 4 for float-based money handling, so run demo 4 first if you want the two to connect. Both then *try* to fix what they found — and fail, because `Edit` isn't available to them (that tool is listed in `disallowed-tools`). Your files are never modified.

Here is the frontmatter presented in the forked skill (`ledger-audit-fork`):

```yaml
---
name: ledger-audit-fork
description: Audit a directory of Python money-handling code for float-based currency arithmetic and report violations of the LR-7 ledger rules.
argument-hint: [path-to-audit]
context: fork
agent: general-purpose
background: false
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, Write, Bash
---
```

The `ledger-audit-inline` is the same except `context`, `agent` and `background` are deleted.

`background: false` makes the forked result land in the same turn you invoked it, instead of arriving later as a notification (asynchronously). For this demo you want that.

Note, `background` requires Claude Code **v2.1.218 or newer** — check with `claude --version`.

Each skill body ends by asking the model to say whether it can see any earlier conversation. That will show us whether the skill is running in an isolated context (i.e. `context: fork`) or the main parent context.

## Run it

**0.** Confirm your version: `claude --version`.

**1.** `/clear`, then plant something the context for the skill to find:

```
Remember that my demo passphrase is `emerald-42`. Don't write this to persistent memory, just remember for this conversation.
```

**2.** Type `/ledger-` into the input box and stop. Autocomplete shows both
skills, each with `[path-to-audit]` beside it. That's `argument-hint` — it does
nothing else, and it's invisible anywhere but here.

**3.** Run the control first:

```
/ledger-audit-inline ccar-f-demos/demo4/app
```

Then run a context report and write down the context usage:

```
/context
```

**4.** Now the forked version:

```
/ledger-audit-fork ccar-f-demos/demo4/app
```

...followed by another context usage report:

```
/context
```

## What to look for

**Step 3 vs Step 4 is the key part of the demo.** It runs the same instructions, but in different contexts:

| | `/ledger-audit-inline` | `/ledger-audit-fork` |
|---|---|---|
| Runs in | your conversation | a forked subagent |
| Sees `emerald-42` | **yes** — quotes it back | **no** — reports no prior conversation |
| What lands in your context | every file it read | just the returned report |

The forked run has no conversation history. It was handed the skill body and nothing else (the prior conversational history was not sent) so it cannot remember the `emerald-42` password.

**In both runs, the fix attempt fails.** The model reaches for `Edit`, finds it isn't in its toolset, and says so. Note that it *tried* — the skill body tells it to attempt the edit and explicitly not to pre-judge whether it's allowed. Nothing in the instructions stops it. The missing tool does.

When running the forked version, the parent context size only grows slightly, reflecting the subagent's final output (a summary it writes at the end of its run). It does not include any intermediate output or reasoning - that is isolated in the fork's context.

## Allowed and disallowed tools

Both `allowed-tools` and `disallowed-tools` last for **the turn that invoked the skill, and no longer**. The docs state: *"The restriction clears when you send your next message."*

After the audits, you could ask a follow-up prompt:

```
Now fix the violations you found.
```

and **it works.** Claude edits the files quite happily. This is a new message, so the restriction lapsed before you asked. The skill's instructions persist in context but its permissions do not.

The other gotcha is the fields are not opposites:

- **`allowed-tools` pre-approves.** It suppresses permission prompts for those tools during the invoking turn. It does not restrict anything. Listing `Read, Grep, Glob` does not mean "only these" — it means "don't ask me before running these".
- **`disallowed-tools` restricts.** It removes tools from Claude's pool for that turn. This is what actually stops the edit.

So `allowed-tools` is why the audit runs without interrupting you for permission, and `disallowed-tools` is why it can't write.