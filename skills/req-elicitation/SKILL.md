# SKILL.md — req-elicitation

> Chains: requirements-agent + nfr-agent → HITL Gate 2
> Registry ID: `suprmans/vibe-spec:req-elicitation`
> Depends on: `vibe-ba` skill output (context.json + vibe-fingerprint.json approved at Gate 1)

---

## What this skill does

Generates the full requirements set from approved org context. Runs `requirements-agent` and `nfr-agent` in parallel, calls Python scoring tools for exact metric computation, then surfaces everything to the human analyst at HITL Gate 2.

---

## Invocation

```
/vibe-spec:req-elicitation "[context.json path]" "[vibe-fingerprint.json path]"
```

---

## Pre-flight checks

Before starting, verify:

1. `context.json` exists at the provided path and is valid JSON
2. `vibe-fingerprint.json` exists and has an `approval_log` entry (Gate 1 was approved)
3. Python tooling is available: `uv run vibe-spec --help`

If Gate 1 has not been approved, stop and tell the human to run `/vibe-spec:vibe-ba` first and complete the Gate 1 review.

```bash
# Check Gate 1 approval
uv run vibe-spec validate context "[context.json path]"
```

---

## Step 1 — Read vibe calibration

Read `vibe-fingerprint.json` and note the calibration rules before generating any requirements:

- `org_maturity` score → plain vs. formal language calibration
- `agility_signal` score → story-first vs. detailed spec calibration
- `process_discipline` score → flag compliance-relevant requirements
- `data_maturity` score → measurability expectations for ACs

---

## Step 2 — Generate user stories (requirements-agent)

Read `agents/requirements-agent.md` and execute the prompt template against `context.json` and `vibe-fingerprint.json`.

For each generated user story, call the scoring tool immediately:

```bash
uv run vibe-spec score-story \
  --text "[story text]" \
  --ac "[acceptance criterion 1]" \
  --ac "[acceptance criterion 2]"
```

Rules:
- If `invest_score < 0.75`: rewrite the story before including it
- If `ambiguity_flag > 0`: fix each flagged phrase before including
- If `ac_coverage < 2`: add acceptance criteria before including
- Do not include any story that fails these checks — fix first, include after

---

## Step 3 — Generate functional requirements (requirements-agent)

From the same requirements-agent run, extract functional requirements (business rules, integration behaviours, data requirements). These do not go through INVEST scoring but must have a measurable criterion.

```bash
# Validate the full requirements artefact
uv run vibe-spec validate requirements "output/[run-id]/requirements-v0.1-[date].md"
```

---

## Step 4 — Generate NFRs (nfr-agent)

Read `agents/nfr-agent.md` and execute the prompt template against `context.json` and `vibe-fingerprint.json`.

For each generated NFR, call the measurability scoring tool:

```bash
uv run vibe-spec score-nfr \
  --category "[category]" \
  --criterion "[measurable criterion text]"
```

Rules:
- If `measurability_score < 0.50`: block the NFR — do not include, return rewrite prompt
- If `measurability_score < 0.80`: include with a flag for human review at Gate 2

---

## Step 5 — Write artefacts

```bash
# Write versioned artefact files
uv run vibe-spec write-artefact requirements "output/[run-id]/" "[requirements json]"
uv run vibe-spec write-artefact nfr-register "output/[run-id]/" "[nfr json]"
```

---

## Step 6 — HITL Gate 2

Present the requirements set to the human analyst using this format:

```
## HITL Gate 2 — Requirements Review

I've generated [N] user stories, [N] functional requirements, and [N] NFRs.
All stories pass INVEST scoring (avg: X.XX). [N] NFRs flagged for measurability review.

### User stories summary

| ID | Title | INVEST | Priority | Confidence |
|---|---|---|---|---|
| REQ-001 | [title] | 0.83 | Must Have | 0.85 |
...

### Functional requirements summary
[N] functional requirements across [categories].

### NFR summary

| ID | Category | Measurability | Priority |
|---|---|---|---|
| NFR-001 | performance | 0.90 | Must Have |
...

⚠ Flagged for review: [list NFRs with measurability 0.50–0.79]

### Your options

- `approve` — proceed to gap analysis with this requirements set
- `modify REQ-XXX [instructions]` — revise a specific story or NFR
- `reject [reason]` — discard and restart with additional context
```

Do not proceed to gap-analysis skill until the human responds with `approve`.

---

## Constitutional checks

- [ ] Article 1: Gate 2 presented, not bypassed
- [ ] Article 3: INVEST scores computed via Python tool (not estimated by AI)
- [ ] Article 4: All stories trace to OBJ- or PAIN- IDs
- [ ] Article 5: Confidence disclosed on all priority assignments
- [ ] Article 7: No requirements invented beyond what context.json contains
