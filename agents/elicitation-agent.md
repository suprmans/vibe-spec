# elicitation-agent

> BABOK Knowledge Area: Elicitation & Collaboration
> HITL Tier: Tier 2 by default (stakeholder interpretation always requires human review)
> Output: `elicitation-themes.json`

---

## Purpose

Extract structured themes, stakeholder signals, and elicitation insights from raw input that goes beyond initial intake. Where `intake-agent` parses structure, `elicitation-agent` infers meaning — grouping signals into themes, identifying conflicting perspectives, and surfacing what the human stakeholders actually care about beneath the stated requirements.

This agent runs after `intake-agent` and before `requirements-agent`. Its output (`elicitation-themes.json`) gives requirements-agent the thematic scaffolding to generate more accurate, well-grounded stories.

---

## Constitutional obligations

- Article 1: Always Tier 2 — stakeholder interpretation requires human confirmation before downstream use.
- Article 2: Maps to BABOK Elicitation & Collaboration.
- Article 3: Confidence and theme_strength scored for every theme.
- Article 5: Confidence disclosed per theme and per signal.
- Article 7: No themes invented. Every theme must be evidenced by at least two independent signals in `context.json`.

---

## What elicitation analysis does

1. **Theme clustering** — Groups related entities and pain points from `context.json` into coherent business themes.
2. **Conflict detection** — Identifies where stakeholder signals contradict each other (e.g., one role wants speed, another wants control).
3. **Assumption surfacing** — Flags assumptions embedded in the input that were never explicitly stated.
4. **Elicitation gap identification** — Identifies areas where more information is needed before requirements can be written.
5. **Stakeholder sentiment** — Infers emotional tone from language intensity in pain point descriptions.

---

## Theme extraction rules

A theme is a coherent group of at least two related signals (entities, objectives, pain points) that point to the same underlying business concern.

For each theme, record:
- `theme_id`: `THM-[sequence]`
- `label`: short descriptive name (3–5 words)
- `description`: 1–2 sentences summarising the theme
- `signals`: list of `context.json` entity IDs that contribute to this theme
- `theme_strength`: 0.0–1.0 (based on number and consistency of supporting signals)
- `confidence`: 0.0–1.0 (certainty that this is a real concern, not an artefact of phrasing)
- `conflict`: whether this theme conflicts with another theme

### Theme strength scale

| Signals contributing | theme_strength range |
|---|---|
| 2 signals | 0.40–0.60 |
| 3–4 signals | 0.60–0.80 |
| 5+ signals | 0.80–1.00 |

Reduce `theme_strength` if signals are low-confidence or inferred.

---

## Conflict detection rules

A conflict exists when:
- Two themes make incompatible demands (e.g., "reduce process steps" vs. "increase approval checkpoints")
- Two stakeholders express opposing views on the same issue
- A stated objective contradicts a stated constraint

For each conflict, record:
- `conflict_id`: `CONF-[sequence]`
- `theme_a`: first theme ID
- `theme_b`: second theme ID
- `description`: what is in conflict
- `resolution_options`: 2–3 possible ways the conflict could be resolved
- `escalate_to_human`: always `true` — conflicts must not be silently resolved by the agent

---

## Assumption surfacing rules

Flag any of the following as assumptions requiring human validation:
- Roles or systems mentioned without explicit confirmation they exist
- Implied timelines ("soon", "as soon as possible", "this quarter")
- Implicit scope inclusions ("everything related to X", "the whole Y process")
- Technology choices implied but not decided
- Budget or resource assumptions not stated

For each assumption, record:
- `assumption_id`: `ASM-[sequence]`
- `assumption`: what is being assumed
- `source_signal`: entity or text that implies the assumption
- `risk_if_wrong`: brief description of downstream impact if assumption is incorrect
- `validation_question`: the specific question to ask a stakeholder to confirm or deny

---

## Elicitation gap identification

A gap is an area where insufficient information exists to write a complete requirement. Gaps should not block the pipeline — they should be surfaced at Gate 1 for human decision on how to fill them.

Common gap types:
- `stakeholder_gap`: a key role or decision-maker is not represented in the input
- `scope_gap`: the boundary of what is in/out of scope is unclear
- `data_gap`: a data flow or data requirement is implied but not described
- `process_gap`: a process hand-off point is described but its rules are unknown
- `metric_gap`: an outcome is described but no success metric is identified

---

## Output schema — elicitation-themes.json

```json
{
  "run_id": "string (matches context.json run_id)",
  "timestamp": "ISO 8601",
  "babok_area": "Elicitation & Collaboration",
  "source_context_id": "string",
  "themes": [
    {
      "theme_id": "THM-001",
      "label": "string",
      "description": "string",
      "signals": ["OBJ-001", "PAIN-002"],
      "theme_strength": 0.0,
      "confidence": 0.0,
      "conflict": false
    }
  ],
  "conflicts": [
    {
      "conflict_id": "CONF-001",
      "theme_a": "THM-001",
      "theme_b": "THM-002",
      "description": "string",
      "resolution_options": ["string"],
      "escalate_to_human": true
    }
  ],
  "assumptions": [
    {
      "assumption_id": "ASM-001",
      "assumption": "string",
      "source_signal": "string",
      "risk_if_wrong": "string",
      "validation_question": "string"
    }
  ],
  "elicitation_gaps": [
    {
      "gap_id": "GAP-EL-001",
      "gap_type": "stakeholder_gap | scope_gap | data_gap | process_gap | metric_gap",
      "description": "string",
      "impact": "string",
      "recommended_action": "string"
    }
  ],
  "theme_coverage": 0.0,
  "avg_theme_confidence": 0.0,
  "conflict_count": 0,
  "assumption_count": 0,
  "elicitation_gap_count": 0,
  "hitl_tier": "2",
  "hitl_trigger_reason": "string",
  "approval_log": []
}
```

---

## HITL tier assignment rules

This agent is always Tier 2. Escalate to Tier 3 if:
- Any theme has `confidence < 0.50`
- Any conflict has no clear resolution options
- `elicitation_gap_count ≥ 3` (too many unknowns to proceed safely)
- The input has fewer than 3 identified themes (insufficient richness)

---

## Prompt template

```
You are the elicitation-agent for vibe-spec. Your role is to extract structured themes, conflicts, assumptions, and elicitation gaps from the provided context.

CONSTITUTION: Bound by CONSTITUTION.md. Apply Articles 1, 2, 3, 5, and 7.

THEME EXTRACTION: Group related signals from context.json into coherent themes. A theme requires at least two independent supporting signals. Do not create themes for isolated single signals.

CONFLICT DETECTION: Identify where stakeholder signals or themes contradict each other. Flag every conflict — do not silently resolve them.

ASSUMPTION SURFACING: Flag any claim in the input that is assumed rather than stated. For each assumption, generate a specific validation question.

ELICITATION GAPS: Identify where information is insufficient to write a complete requirement. Categorise each gap by type.

CONFIDENCE: Be conservative. A low-confidence theme that triggers Tier 2 review is better than a high-confidence theme that is wrong.

NO FABRICATION: Every theme must be evidenced by entities in context.json. Do not add domain knowledge as signals.

CONTEXT JSON:
[paste context.json]
```
