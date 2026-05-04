# SKILL.md — vibe-ba

> Distributable Claude skill: Org vibe analysis
> Chains: intake-agent → vibe-analyzer → HITL Gate 1
> Registry ID: `suprmans/vibe-spec:vibe-ba`

---

## What this skill does

`vibe-ba` takes raw business context and produces two structured artefacts:
1. `context.json` — parsed and structured entities from the input (intake-agent)
2. `vibe-fingerprint.json` — 6-dimension org maturity profile (vibe-analyzer)

It then surfaces the vibe fingerprint to the human analyst for review (HITL Gate 1) before signalling readiness for the requirements phase.

This is the entry point to the vibe-spec pipeline. Run this first.

---

## Invocation

```
/vibe-spec:vibe-ba "[your business context here]"
```

Or from the marketplace:
```
/plugin marketplace add suprmans/vibe-spec
/vibe-spec:vibe-ba "[your business context here]"
```

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `context` | Yes | Raw business input: meeting notes, problem statement, process description, or stakeholder brief |

---

## Outputs

| File | Description |
|---|---|
| `context.json` | Structured entities extracted from input |
| `vibe-fingerprint.json` | 6-dimension org vibe scores with confidence values |

---

## Execution steps

**Step 1 — Intake parsing**

Read `agents/intake-agent.md` and execute the intake prompt against the provided input.

Emit `context.json`. Check:
- HITL tier assigned correctly
- All entity arrays populated or explicitly empty with `insufficient_input_flags`
- `intake_confidence` computed

If `intake_confidence < 0.60`: surface Tier 3 flag to human before proceeding to Step 2.

**Step 2 — Vibe analysis**

Read `agents/vibe-analyzer.md` and execute the vibe-analyzer prompt against `context.json`.

Emit `vibe-fingerprint.json`. Check:
- All 6 dimensions scored
- Signals listed per dimension
- `tier3_dimensions` populated if any dimension confidence < 0.60
- BA archetype classified with rationale
- Red flags identified

**Step 3 — HITL Gate 1**

Present the vibe fingerprint to the human in this format:

```
## HITL Gate 1 — Org Context Review

I've analysed the input and produced an org vibe fingerprint. Please review and confirm before I proceed to requirements generation.

### Vibe fingerprint summary

| Dimension | Score | Confidence | Interpretation |
|---|---|---|---|
| org_maturity | X.X | X.XX | [interpretation] |
| agility_signal | X.X | X.XX | [interpretation] |
| political_density | X.X | X.XX | [interpretation] |
| process_discipline | X.X | X.XX | [interpretation] |
| change_readiness | X.X | X.XX | [interpretation] |
| data_maturity | X.X | X.XX | [interpretation] |

**BA archetype:** [type] — [rationale]

**Red flags identified:** [list or "None"]

**Low-confidence dimensions (< 0.60):** [list or "None — all dimensions above threshold"]

### Your options

- `approve` — proceed to requirements generation with this fingerprint
- `modify [instructions]` — I'll revise the fingerprint per your instructions
- `reject [reason]` — discard and restart with additional context
```

Do not proceed to `requirements-agent` until the human responds with `approve` or `modify` (after modification).

---

## Constitutional checks for this skill

Before emitting either output:
- [ ] Article 1: Tier 2 HITL applied to vibe-fingerprint. Gate 1 presented before proceeding.
- [ ] Article 2: Both outputs carry correct `babok_area` fields.
- [ ] Article 3: All 6 dimension scores present in vibe-fingerprint. `intake_confidence` present in context.json.
- [ ] Article 5: Confidence disclosed for every score. Low-confidence dimensions flagged.
- [ ] Article 7: No entities or signals invented. All derived from input.

---

## Error states

| Condition | Response |
|---|---|
| Input too short (< 50 words) | Return `insufficient_input` with guidance on what to provide |
| No business objective identifiable | Return `insufficient_input` — cannot proceed without at least one objective |
| All 6 vibe dimensions have confidence < 0.60 | Escalate to Tier 3, present to human with explicit note that fingerprint has low reliability |
| Human rejects at Gate 1 | Ask what was incorrect; offer to re-run with corrected context or human-authored vibe scores |
