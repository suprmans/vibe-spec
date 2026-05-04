# HITL Review Template

Use this template at every HITL gate. Fill in the gate number, artefact summary, and options block.

---

## Gate [N] — [Gate name]

> Tier [1|2|3] review | Agent: [agent name] | Run ID: [uuid]

[1–2 sentence summary of what was produced and any notable flags.]

### Artefact summary

[Table or bullet list summarising the key outputs. Keep it scannable — the human should be able to review in under 2 minutes for a typical input.]

### Flags requiring attention

[List any items with confidence < 0.60, measurability_score < 0.80, ambiguity_flags > 0, or engagement_risk: high. If none, write "None — all items within acceptable thresholds."]

### Your options

| Command | Effect |
|---|---|
| `approve` | Accept artefact as-is and proceed to next stage |
| `modify [ID] [instructions]` | Revise a specific item; re-present when done |
| `reject [reason]` | Discard artefact; return to generating agent with feedback |

**Awaiting your decision before proceeding.**

---

## Approval log format

When the human approves (or after modification is accepted), append this block to the artefact file before committing:

```
## Approval log

- timestamp: [ISO 8601]
  hitl_tier: [1|2|3]
  gate: [1|2|3|4]
  reviewer: [name or identifier]
  action: approved | modified | rejected
  modification_note: [description of changes, or null]
```
