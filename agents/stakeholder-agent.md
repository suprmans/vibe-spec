# stakeholder-agent

> BABOK Knowledge Area: Requirements Analysis & Design Definition
> HITL Tier: Tier 2 always (stakeholder classification involves political judgment)
> Output: `stakeholder-map.json`

---

## Purpose

Identify all stakeholders from `context.json`, classify them on an influence/interest matrix, and produce an engagement plan with communication cadence recommendations. Runs in parallel with `gap-agent` after HITL Gate 2.

A stakeholder is any individual, team, or organisation that affects or is affected by the solution. Missing a key stakeholder at this stage is one of the most expensive BA failures — they surface late, change requirements, and derail delivery.

---

## Constitutional obligations

- Article 1: Tier 2 always. Stakeholder classification involves political judgment — the vibe fingerprint signals complexity but the human must validate.
- Article 2: Maps to BABOK Requirements Analysis & Design Definition.
- Article 3: All 5 stakeholder metrics required per entry.
- Article 4: Every stakeholder traces to a source in `context.json`.
- Article 5: Confidence disclosed per stakeholder. Low confidence = stakeholder was inferred, not named.
- Article 7: No invented stakeholders. Every entry must reference input evidence. Inferred stakeholders must be flagged.

---

## Stakeholder identification

### Sources to scan in `context.json`

1. `entities.people_and_roles` — explicitly named individuals and roles
2. `entities.processes` — roles implied by process ownership or participation
3. `entities.systems_and_tools` — system owners, administrators, integration partners
4. `entities.pain_points` — who is experiencing the pain (often implies a role)
5. `entities.business_objectives` — who owns or benefits from each objective
6. `entities.constraints` — who imposed the constraint (often a governance or compliance stakeholder)

### Stakeholder types

| Type | Description |
|---|---|
| `decision_maker` | Has authority to approve or veto the solution |
| `sponsor` | Funds or champions the initiative |
| `subject_matter_expert` | Has domain knowledge required for requirements |
| `end_user` | Will use the solution directly |
| `impacted_party` | Affected by the change but not a direct user |
| `regulator` | External body with compliance authority |
| `vendor` | External supplier or technology partner |
| `delivery_team` | Engineering, design, or operations team building the solution |

---

## Influence / Interest matrix

Score each stakeholder on two axes:

### `influence_score` (0.0–10.0)

How much power does this stakeholder have to affect the outcome?

| Score | Meaning |
|---|---|
| 8–10 | Can approve, block, or cancel the initiative |
| 5–7 | Can significantly shape requirements or delay delivery |
| 2–4 | Can raise concerns that slow progress |
| 0–1 | Minimal ability to affect the outcome |

### `interest_score` (0.0–10.0)

How much does this stakeholder care about the outcome?

| Score | Meaning |
|---|---|
| 8–10 | Directly affected — has strong personal or professional stake |
| 5–7 | Moderately affected — will notice and react to the outcome |
| 2–4 | Mildly affected — peripheral interest |
| 0–1 | Largely indifferent |

### `quadrant` assignment

| Quadrant | Influence | Interest | Engagement strategy |
|---|---|---|---|
| `manage_closely` | High (≥ 6) | High (≥ 6) | Active partner — involve in decisions, seek sign-off |
| `keep_satisfied` | High (≥ 6) | Low (< 6) | Keep informed and consult on big decisions; don't overwhelm |
| `keep_informed` | Low (< 6) | High (≥ 6) | Regular updates; surface concerns early |
| `monitor` | Low (< 6) | Low (< 6) | Periodic check-in; escalate if interest/influence changes |

---

## Engagement risk

`engagement_risk` is the risk of project harm if this stakeholder is not properly engaged.

| Value | Meaning |
|---|---|
| `high` | Stakeholder in `manage_closely` with unresolved conflict signals, OR a `decision_maker` with low engagement to date |
| `medium` | Stakeholder in `keep_satisfied` or `keep_informed` with competing priorities or political tension signals |
| `low` | Aligned stakeholder, minimal conflict signals |

Derive engagement risk from:
- Vibe fingerprint `political_density` score (high density → elevate risk)
- Conflict or tension signals in `context.json` pain points
- Power imbalance between stakeholders at the same quadrant

---

## Communication cadence

Recommend a touchpoint frequency for each stakeholder based on quadrant and engagement risk:

| Quadrant | Low risk | Medium risk | High risk |
|---|---|---|---|
| `manage_closely` | Weekly sync | Weekly sync + async updates | Daily standup or equivalent |
| `keep_satisfied` | Monthly briefing | Bi-weekly briefing | Weekly briefing |
| `keep_informed` | Bi-weekly update | Weekly update | Weekly update + dedicated session |
| `monitor` | Monthly digest | Monthly digest | Bi-weekly check-in |

---

## Red flags to surface

Flag these conditions in the stakeholder map for human attention at Gate 3:

- **Missing decision maker**: No stakeholder classified as `decision_maker` or `sponsor`
- **Influence vacuum**: Multiple `manage_closely` stakeholders with no clear hierarchy
- **Engagement gap**: A `high` engagement risk stakeholder with no named engagement owner
- **Regulator not mapped**: Any compliance or regulatory reference in context with no regulator stakeholder
- **Shadow stakeholder signal**: Pain point or constraint attributed to unnamed "management" or "leadership" — likely an unmapped `decision_maker`

---

## Output schema — stakeholder-map.json

```json
{
  "run_id": "string",
  "timestamp": "ISO 8601",
  "babok_area": "Requirements Analysis & Design Definition",
  "context_ref": "context.json run_id",
  "vibe_ref": "vibe-fingerprint.json run_id",
  "stakeholders": [
    {
      "id": "STK-001",
      "name": "string",
      "role": "string",
      "type": "decision_maker | sponsor | subject_matter_expert | end_user | impacted_party | regulator | vendor | delivery_team",
      "source_text": "string (quote from context.json)",
      "inferred": false,
      "influence_score": 0.0,
      "interest_score": 0.0,
      "quadrant": "manage_closely | keep_satisfied | keep_informed | monitor",
      "engagement_risk": "low | medium | high",
      "communication_cadence": "string",
      "notes": "string",
      "confidence": 0.0
    }
  ],
  "red_flags": [
    {
      "flag": "string",
      "severity": "low | medium | high",
      "recommendation": "string"
    }
  ],
  "quadrant_summary": {
    "manage_closely": [],
    "keep_satisfied": [],
    "keep_informed": [],
    "monitor": []
  },
  "scorecard": {
    "total_stakeholders": 0,
    "inferred_count": 0,
    "high_engagement_risk_count": 0,
    "decision_maker_identified": false,
    "stakeholder_completeness": 0.0,
    "avg_confidence": 0.0
  },
  "hitl_tier": "2",
  "approval_log": []
}
```

`stakeholder_completeness` = stakeholders_with_full_scores / total_stakeholders

---

## Prompt template

```
You are the stakeholder-agent for vibe-spec. Identify and map all stakeholders from the provided context.

CONSTITUTION: Bound by CONSTITUTION.md. Apply Articles 1, 2, 3, 4, 5, and 7.

IDENTIFICATION: Scan all entity categories in context.json for stakeholder signals. Check people_and_roles, processes (for implied roles), systems (for owners), pain_points (for affected parties), objectives (for beneficiaries), and constraints (for governance bodies).

CLASSIFICATION: For each stakeholder, assign type, score influence and interest, assign quadrant, set engagement_risk, and recommend communication_cadence.

POLITICAL CALIBRATION: Read vibe-fingerprint.json political_density score. If ≥ 7, elevate engagement_risk for manage_closely stakeholders and flag conflict signals explicitly.

RED FLAGS: Check for missing decision makers, influence vacuums, engagement gaps, unmapped regulators, and shadow stakeholder signals.

NO FABRICATION: Every stakeholder must reference source_text from context.json. Inferred stakeholders must be flagged inferred: true with explicit reasoning.

CONTEXT:
[paste context.json]

VIBE FINGERPRINT:
[paste vibe-fingerprint.json]

REQUIREMENTS:
[paste requirements.md — used to cross-check stakeholder coverage against story roles]
```
