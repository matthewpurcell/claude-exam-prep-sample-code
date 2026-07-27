# Demo 6 — Enforcing a JSON schema with structured outputs

Unlike demos 4 and 5, this one **is** a notebook. It needs the Python virtual
environment and an Anthropic API key — follow the setup in the [root README](../../README.md)
first.

Uses the Anthropic SDK directly (`anthropic`), like demos 1 and 3. Structured
outputs are a Messages API feature, so schema enforcement lives on the raw SDK —
the Claude Agent SDK used in demo 2 wraps the Claude Code harness and doesn't
expose request-level output config.

## What this demo shows

Structured outputs constrain a response to a JSON Schema you supply. The reply is
guaranteed to parse and guaranteed to match the shape you asked for.

That guarantee is narrower than it sounds. A field you mark required with no escape
hatch is a field the model **must** fill in — and if the source doesn't contain the
answer, it will supply one anyway. The result passes validation, because there was
never anything malformed to catch.

So the demo isn't really about attaching a schema. It's about the sharper thing
underneath: **a schema guarantees shape, not truth.**

## Files

```
ccar-f-demos/demo6/structured_outputs.ipynb
```

Four support tickets run through two schemas. Same model, same system prompt, same
tickets — the schema is the only variable, in the style of demo 3.

The **naive schema** has three tight enums and a plain number, everything required:

```python
"category":      {"enum": ["billing", "shipping", "technical"]},
"priority":      {"enum": ["low", "medium", "high"]},
"refund_amount": {"type": "number"},
```

The **escape-hatch schema** changes three things:

```python
"category":       {"enum": ["billing", "shipping", "technical", "other"]},
"category_other": {"anyOf": [{"type": "string"}, {"type": "null"}]},
"priority":       {"enum": ["low", "medium", "high", "not_stated"]},
"refund_amount":  {"anyOf": [{"type": "number"}, {"type": "null"}]},
```

## Run it

Run the cells top to bottom. The interesting part is section 3, which prints both
runs side by side.

## What to look for

Three of the four tickets are engineered so the naive schema has no honest answer
available. From an actual run:

| ticket | naive schema | escape-hatch schema |
|---|---|---|
| 1 · double charge (control) | `billing`, `high`, `49.99` | identical |
| 2 · partnership enquiry | `billing`, `low`, `0` | `other` + *"Business/reseller partnership inquiry"*, `not_stated`, `null` |
| 3 · delivery windows | `shipping`, `low`, `0` | `shipping`, `not_stated`, `null` |
| 4 · damaged twice | `shipping`, `high`, `0` | `shipping`, `high`, `null` |

The partnership enquiry is the one to point at: under the naive schema it comes back
as a **billing** ticket requesting a **$0 refund**. Wrong on both counts, and perfectly
valid JSON.

Note what `0` is doing in that column. It isn't "unknown" — it's a claim that the
customer asked for nothing. A downstream report summing `refund_amount` would never
notice the difference.

And the control ticket matters as much as the failures: where the source genuinely
contains the answer, both schemas agree exactly. The escape hatches don't make the
model vaguer, they only give it somewhere to put a gap.

## The three patterns

| pattern | JSON Schema | use when |
|---|---|---|
| **Nullable field** | `anyOf: [{...}, {"type": "null"}]` | the value may genuinely not exist |
| **`other` + companion** | extra enum member + nullable string sibling | your enum can't be exhaustive |
| **Sentinel member** | `"not_stated"` in the enum | a value exists but the source is silent |

`null` and `not_stated` are not the same thing and shouldn't be collapsed into one.
`null` means *no value exists*. `not_stated` means *a value exists, but this document
doesn't give it* — every ticket has some real urgency, ticket 3 just doesn't say what
it is. Conflating them is a modelling error you have to unpick later.

An `other` enum member on its own is also only half a fix: it records that your enum
failed, then throws away what the thing actually was. Pair it with a nullable free-text
sibling.

## Notes

- **The parameter is `output_config={"format": {...}}`.** The old top-level
  `output_format` on `messages.create()` is deprecated — as of `anthropic` 0.120.0 it
  isn't even accepted as a keyword argument any more.
- **`output_config` also carries `effort`**, so `{"effort": "low", "format": {...}}` is
  one dict. Extraction doesn't need deep reasoning and `low` keeps eight live API calls
  quick.
- **`required` must list every property**, and `additionalProperties` must be `false`.
  You cannot make a field optional by omitting it from `required` — optionality is
  expressed in the type, with a `null` branch. This is the detail people get wrong first.
- `{"type": ["number", "null"]}` is accepted and means the same as the `anyOf` form. The
  notebook uses `anyOf` because it stays readable when the non-null branch is more than a
  bare type.
- **The first request against a new schema pays a one-off compilation cost**, then caches
  for 24 hours. Don't be alarmed by a slow first cell on stream.
- `output_config.format` is incompatible with citations — that combination returns a 400.
