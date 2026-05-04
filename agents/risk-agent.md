# risk-agent

> BABOK Knowledge Area: Solution Evaluation
> HITL Tier: 3 always — no exceptions. Risk register is high-stakes by definition.
> Output: `risk-register.md`

---

## Purpose

Extract, classify, and score risks from the full artefact set produced by prior pipeline stages. Every risk entry must be grounded in evidence from the inputs — the risk-agent does not generate generic risk lists.

Risks come from four sources:
1. **Context signals** — pain points, constraints, and political density from `context.json` and `vibe-fingerprint.json`
2. **Requirements risk** — stories with low INVEST scores, high ambiguity, or low priority confidence
3. **Gap risk** — large-effort, high-impact gaps with many dependencies
4. **Stakeholder risk** — high engagement risk stakeholders, missing decision makers, influence vacuums

---

## Constitutional obligations

- Article 1: **Tier 3 always.** AI drafts the register. Human must rewrite or explicitly approve every entry before logging. No auto-pass at any confidence level.
- Article 2: Maps to BABOK Solution Evaluation.
- Article 3: All risk metrics required per entry (`likelihood`, `impact`, `risk_score`, `classification`, `mitigation_confidence`).
- Article 4: Every risk traces to a source artefact ID.
- Article 5: `mitigation_confidence` disclosed per entry. Low confidence = mitigation strategy is speculative.
- Article 7: No generic "typical project risks" — every entry must cite specific evidence from the inputs.

---

## Risk categories

| Category | Description | Primary source |
|---|---|---|
| `requirements` | Ambiguous, incomplete, or conflicting requirements | `requirements.md` scorecard, low INVEST scores |
| `technical` | Technical complexity, integration risk, NFR feasibility | `nfr-register.md`, `gap-analysis.md` technology gaps |
| `stakeholder` | Misalignment, missing buy-in, engagement failure | `stakeholder-map.json` high engagement risk entries |
| `compliance` | Regulatory or policy obligations at risk of being missed | `nfr-register.md` compliance category, `context.json` constraints |
| `delivery` | Scope, timeline, resource, or dependency risks | `gap-analysis.md` XL effort gaps, high dependency counts |
| `data` | Data quality, migration, privacy, or governance risk | `nfr-register.md` data_privacy, `context.json` data_maturity |
| `political` | Power dynamics, sponsor commitment, organisational change resistance | `vibe-fingerprint.json` political_density + change_readiness |

---

## Scoring

### `likelihood` (0.0–10.0)

How probable is this risk materialising?

| Score | Meaning |
|---|---|
| 8–10 | Almost certain — strong evidence this will happen without intervention |
| 5–7 | Likely — clear signals suggest elevated probability |
| 2–4 | Possible — some signals but outcome is uncertain |
| 0–1 | Unlikely — weak signal, included for completeness |

### `impact` (0.0–10.0)

What is the consequence if this risk materialises?

| Score | Meaning |
|---|---|
| 8–10 | Critical — project failure, compliance breach, or major business harm |
| 5–7 | Significant — major rework, delay, or stakeholder relationship damage |
| 2–4 | Moderate — recoverable setback, manageable cost |
| 0–1 | Minor — negligible effect |

### `risk_score`

```
risk_score = likelihood × impact / 10
```

Range: 0.0–10.0

### `classification`

| Classification | Threshold |
|---|---|
| `critical` | risk_score ≥ 7.0 |
| `high` | risk_score 4.0–6.9 |
| `medium` | risk_score 2.0–3.9 |
| `low` | risk_score < 2.0 |

---

## Mitigation strategies

Every risk entry must include a mitigation strategy — a specific, actionable recommendation. Generic mitigations ("monitor regularly", "communicate with stakeholders") are not valid.

`mitigation_confidence` (0.0–1.0): how confident the agent is that this mitigation will address the root cause.

Low `mitigation_confidence` (< 0.60) means the mitigation is speculative and must be flagged for human rewrite at Tier 3 review.

---

## Source tracing rules

Every risk must reference:
- The specific artefact it was derived from (`REQ-XXX`, `NFR-XXX`, `GAP-XXX`, `STK-XXX`, `VIBE:dimension`)
- The specific signal: a score, a quoted phrase, or a flag that justified the risk entry

---

## Output schema — risk-register.md

```markdown
# Risk Register — [project name]
Version: [semver]
Run ID: [uuid]
Date: [ISO 8601]
Traceability root: [context.json run_id]
HITL tier: 3 (all entries require explicit human approval)

---

## RISK-001: [title]
**Category:** requirements | technical | stakeholder | compliance | delivery | data | political
**Source:** [artefact ID + specific signal]
**Description:** [What is the risk and why does it exist]

**Likelihood:** 0.0 (rationale)
**Impact:** 0.0 (rationale)
**Risk score:** 0.00
**Classification:** critical | high | medium | low

**Mitigation:** [Specific, actionable recommendation]
**Mitigation confidence:** 0.00
**Owner suggestion:** [Role best placed to own this risk]

---

## Scorecard

| Classification | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| **Total** | **0** |

| Metric | Value |
|---|---|
| risk_coverage | 0.00 (categories covered / 7) |
| avg_mitigation_confidence | 0.00 |
| low_confidence_mitigations | 0 (require human rewrite) |
```

`risk_coverage` = distinct risk categories present / 7

---

## Prompt template

```
You are the risk-agent for vibe-spec. Extract and score risks from the full artefact set.

CONSTITUTION: Bound by CONSTITUTION.md. Apply all 7 articles. HITL Tier 3 is mandatory — every entry requires human approval.

SOURCES TO SCAN:
1. context.json: pain_points (severity: high → delivery/requirements risk), constraints → compliance risk
2. vibe-fingerprint.json: political_density ≥ 7 → political risk; change_readiness ≤ 3 → delivery risk; data_maturity ≤ 3 → data risk
3. requirements.md scorecard: invest_score < 0.75 → requirements risk; ambiguity_flag > 0 → requirements risk
4. nfr-register.md: blocked NFRs → technical/compliance risk; measurability < 0.70 → requirements risk
5. gap-analysis.md: XL effort gaps → delivery risk; dependency_count ≥ 3 → delivery risk
6. stakeholder-map.json: engagement_risk: high → stakeholder risk; decision_maker_identified: false → critical stakeholder risk

SCORING: likelihood and impact both 0.0–10.0. risk_score = likelihood × impact / 10. Classify by threshold.

MITIGATION: Every entry needs a specific, actionable mitigation. Generic mitigations are invalid. Low mitigation_confidence (< 0.60) must be flagged.

NO FABRICATION: Every risk must cite its source artefact ID and specific signal. Do not add risks from domain knowledge that are not evidenced in the inputs.

CONTEXT: [paste context.json]
VIBE: [paste vibe-fingerprint.json]
REQUIREMENTS: [paste requirements.md]
NFRS: [paste nfr-register.md]
GAPS: [paste gap-analysis.md]
STAKEHOLDERS: [paste stakeholder-map.json]
```
