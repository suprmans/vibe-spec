# SKILL.md — gap-analysis

> Chains: gap-agent + stakeholder-agent (parallel) → HITL Gate 3
> Registry ID: `suprmans/vibe-spec:gap-analysis`
> Depends on: `req-elicitation` skill output (requirements.md + nfr-register.md approved at Gate 2)

---

## What this skill does

Runs `gap-agent` and `stakeholder-agent` in parallel after Gate 2 approval. Produces a prioritised gap register and stakeholder map, validates both artefacts, then surfaces them together at HITL Gate 3 for strategic alignment review.

---

## Invocation

```
/vibe-spec:gap-analysis "[requirements.md path]" "[context.json path]" "[vibe-fingerprint.json path]"
```

---

## Pre-flight checks

```bash
# Verify Gate 2 was approved
uv run vibe-spec validate requirements "[requirements.md path]"
```

If `requirements.md` has no `approval_log` entry, stop. Tell the human to run `/vibe-spec:req-elicitation` first and complete Gate 2.

---

## Step 1 — Run gap-agent and stakeholder-agent in parallel

Read `agents/gap-agent.md` and `agents/stakeholder-agent.md`. Execute both prompt templates simultaneously against the provided inputs.

Gap agent inputs: `requirements.md` + `context.json`
Stakeholder agent inputs: `context.json` + `vibe-fingerprint.json` + `requirements.md`

---

## Step 2 — Score and validate gaps

For each identified gap:

```bash
uv run vibe-spec score-gap \
  --trace-id "[REQ-XXX or PAIN-XXX]" \
  --effort "[XS|S|M|L|XL]" \
  --impact "[0.0-10.0]"
```

This returns: `quick_win_flag`, validated `priority_tier`, `dependency_warnings`.

After all gaps are scored:

```bash
uv run vibe-spec validate gap-analysis "output/[run-id]/gap-analysis-v0.1-[date].md"
```

---

## Step 3 — Validate stakeholder map

```bash
uv run vibe-spec validate stakeholder-map "output/[run-id]/stakeholder-map-v0.1-[date].json"
```

Checks:
- At least one `decision_maker` or `sponsor` stakeholder present
- All stakeholders have quadrant + engagement_risk assigned
- Red flags documented

---

## Step 4 — Write artefacts

```bash
uv run vibe-spec write-artefact gap-analysis "output/[run-id]/" "[gap json]"
uv run vibe-spec write-artefact stakeholder-map "output/[run-id]/" "[stakeholder json]"
```

---

## Step 5 — HITL Gate 3

Present both artefacts together for strategic alignment review:

```
## HITL Gate 3 — Strategic Alignment Review

Gap analysis and stakeholder map are ready for your review.

### Gap summary

[N] gaps identified across [types].

Quick wins ([N]):
| ID | Title | Impact | Effort |
|---|---|---|---|
| GAP-001 | [title] | 8.5 | S |

Strategic bets ([N]):
| ID | Title | Impact | Effort |
|---|---|---|---|
| GAP-003 | [title] | 9.0 | L |

### Stakeholder summary

| Quadrant | Count | High engagement risk |
|---|---|---|
| Manage closely | N | N |
| Keep satisfied | N | N |
| Keep informed | N | N |
| Monitor | N | N |

⚠ Red flags: [list or "None"]

### Strategic alignment check

Do these gaps and stakeholders reflect your understanding of the business context?
Are any critical gaps missing? Are any stakeholders misclassified?

### Your options

- `approve` — proceed to risk analysis with this gap + stakeholder set
- `modify GAP-XXX [instructions]` — adjust a gap priority or classification
- `modify STK-XXX [instructions]` — adjust a stakeholder quadrant or risk level
- `reject [reason]` — discard and restart with additional context
```

Do not proceed to `risk-agent` until the human responds with `approve`.

---

## Constitutional checks

- [ ] Article 1: Gate 3 presented, not bypassed
- [ ] Article 3: `gap_coverage` and `stakeholder_completeness` scores computed
- [ ] Article 4: All gaps trace to REQ-, FR-, PAIN-, or OBJ- IDs
- [ ] Article 5: Confidence disclosed on all gap scores and stakeholder classifications
- [ ] Article 7: No gaps or stakeholders invented — all derived from inputs
