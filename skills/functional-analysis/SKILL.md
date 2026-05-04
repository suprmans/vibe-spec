# SKILL.md — functional-analysis

> Chains: elicitation-agent → requirements-agent + nfr-agent → HITL Gate 2
> Registry ID: `suprmans/vibe-spec:functional-analysis`
> Depends on: `vibe-ba` skill output (context.json + vibe-fingerprint.json approved at Gate 1)

---

## What this skill does

Runs the full functional + non-functional analysis layer. Takes approved org context and vibe fingerprint, extracts elicitation themes, then generates INVEST-scored user stories, functional requirements, and measurability-scored NFRs in one pass.

Use this skill when you want the complete functional specification — requirements and NFRs together — in a single invocation without running `req-elicitation` and `gap-analysis` separately.

---

## Invocation

```
/vibe-spec:functional-analysis "[context.json path]" "[vibe-fingerprint.json path]"
```

---

## Pre-flight checks

Before starting, verify:

1. `context.json` exists and is valid
2. `vibe-fingerprint.json` has an `approval_log` entry (Gate 1 completed)
3. Python tooling: `uv run vibe-spec --help`

```bash
uv run vibe-spec validate context "[context.json path]" --json
```

Stop and report if Gate 1 has not been approved. Do not generate requirements from unapproved context.

---

## Step 1 — Elicitation theme extraction

Read `agents/elicitation-agent.md` and execute the prompt template against `context.json`.

Output: structured theme list with `theme_strength`, conflicts, assumptions, and elicitation gaps.

Review conflicts and elicitation gaps before proceeding:
- If `conflict_count > 0`: note each conflict and its resolution options for Gate 2 presentation
- If `elicitation_gap_count ≥ 3`: surface all gaps at Gate 2 rather than proceeding silently
- If any theme has `confidence < 0.50`: flag it for human attention

---

## Step 2 — Vibe calibration

Read `vibe-fingerprint.json` and apply calibration before generating requirements:

| Vibe signal | Applied calibration |
|---|---|
| `org_maturity ≤ 3` | Plain language, short stories, minimal formal notation |
| `org_maturity ≥ 7` | Formal IDs, traceability tags, reference standards |
| `agility_signal ≥ 7` | Story-first, minimal prose |
| `agility_signal ≤ 3` | Detailed functional specs alongside stories |
| `process_discipline ≥ 7` | Flag compliance-relevant requirements explicitly |
| `data_maturity ≥ 7` | Measurable ACs with specific metrics |
| `data_maturity ≤ 3` | Flag stories lacking measurable ACs |

---

## Step 3 — User stories

Read `agents/requirements-agent.md` (Section 1) and generate user stories.

For every story, call the scoring tool immediately:

```bash
uv run vibe-spec score-story \
  --text "[story text]" \
  --ac "[acceptance criterion 1]" \
  --ac "[acceptance criterion 2]" \
  --json
```

Rules:
- `invest_score < 0.75`: rewrite before including
- `ambiguity_flag > 0`: fix each flagged phrase before including
- `ac_coverage < 2`: add ACs before including
- All three checks must pass before a story is included in the output

---

## Step 4 — Functional requirements

From the same requirements-agent run, extract functional requirements (business rules, integration behaviours, data requirements, reporting, admin).

Every functional requirement must have:
- A measurable criterion: how to verify it is met
- A traceability link to `OBJ-` or `PAIN-` in `context.json`
- Priority with confidence score

```bash
uv run vibe-spec validate requirements "output/[run-id]/requirements-v0.1-[date].md" --json
```

---

## Step 5 — NFR analysis

Read `agents/nfr-agent.md` and generate NFRs calibrated to the org's vibe.

For every NFR, call the measurability scoring tool:

```bash
uv run vibe-spec score-nfr \
  --category "[category]" \
  --criterion "[criterion text]" \
  --json
```

Rules:
- `measurability_score < 0.50`: **blocked** — do not include, return rewrite prompt
- `0.50 ≤ measurability_score < 0.80`: include with a `⚠ review` flag
- `measurability_score ≥ 0.80`: include as passing

NFR categories to cover (generate at least one where context supports it):
`performance`, `security`, `availability`, `scalability`, `usability`, `compliance`, `maintainability`, `interoperability`, `data_privacy`

---

## Step 6 — Write artefacts

```bash
uv run vibe-spec write-artefact requirements "output/[run-id]/" "[requirements json]" --json
uv run vibe-spec write-artefact nfr-register "output/[run-id]/" "[nfr json]" --json
```

---

## Step 7 — HITL Gate 2

Present the full functional analysis to the human analyst:

```
## HITL Gate 2 — Functional Analysis Review

### Elicitation summary
Themes identified: [N] | Conflicts: [N] | Assumptions: [N] | Gaps: [N]
[List any conflicts and assumptions requiring human validation]

### User stories
[N] stories generated. Avg INVEST: [X.XX]. All pass threshold: [yes/no]

| ID | Title | INVEST | Priority | Confidence |
|---|---|---|---|---|
| REQ-001 | [title] | 0.83 | Must Have | 0.85 |
...

### Functional requirements
[N] FRs across [categories].

| ID | Category | Priority | Measurable |
|---|---|---|---|
| FR-001 | business_rule | Must Have | yes |
...

### NFRs
[N] NFRs. [N] pass measurability. [N] flagged for review.

| ID | Category | Measurability | Status |
|---|---|---|---|
| NFR-001 | performance | 0.90 | ✓ pass |
| NFR-002 | usability | 0.65 | ⚠ review |
...

### Elicitation gaps requiring decisions
[List any gaps that need stakeholder input before gap analysis]

### Your options

- `approve` — proceed to gap analysis and stakeholder mapping
- `modify REQ-XXX [instructions]` — revise a specific item
- `reject [reason]` — discard and restart with additional context
```

Do not proceed to `gap-analysis` skill until the human responds with `approve`.

---

## Constitutional checks

Before presenting Gate 2:

- [ ] Article 1: Gate 2 will be presented, not bypassed
- [ ] Article 3: All INVEST and measurability scores computed via CLI tools, not estimated
- [ ] Article 4: All stories and FRs trace to OBJ- or PAIN- IDs
- [ ] Article 5: Confidence disclosed on all priority and theme assignments
- [ ] Article 7: No requirements invented beyond what context.json contains

---

## Difference from req-elicitation

| | `req-elicitation` | `functional-analysis` |
|---|---|---|
| Elicitation themes | No | Yes — explicit theme extraction step |
| Conflict detection | No | Yes — surfaced at Gate 2 |
| Assumption audit | No | Yes — each assumption gets a validation question |
| User stories | Yes | Yes |
| Functional requirements | Yes | Yes |
| NFRs | Yes | Yes |
| Best for | Known context, fast pipeline | Complex input, multiple stakeholders, conflicting signals |
