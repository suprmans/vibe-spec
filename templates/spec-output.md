# Spec Output Template

Standard format for all vibe-spec artefact files. Every artefact must include the header block and approval log section.

---

## Header block (required on all artefacts)

```markdown
# [Artefact type] — [Project or context name]

| Field | Value |
|---|---|
| Version | 0.1 |
| Run ID | [uuid] |
| Date | [YYYY-MM-DD] |
| Agent | [agent name] |
| BABOK area | [knowledge area] |
| HITL tier | [1|2|3] |
| Traceability root | [context.json run_id] |
| spec_health (at time of generation) | [score or pending] |
```

---

## Artefact body

[Agent-specific content goes here. See individual agent specs for section structure.]

---

## Scorecard

```markdown
## Scorecard

| Metric | Value | Target | Status |
|---|---|---|---|
| [metric name] | [value] | [target] | PASS / FAIL / REVIEW |
```

---

## Approval log

```markdown
## Approval log

_Pending Gate [N] review._
```

When approved, the agent appends:

```markdown
## Approval log

- timestamp: [ISO 8601]
  hitl_tier: [1|2|3]
  gate: [1|2|3|4]
  reviewer: [name or identifier]
  action: approved | modified | rejected
  modification_note: [description or null]
```

---

## Naming convention

Per CONSTITUTION Article 6.5:

```
[artefact-type]-v[version]-[YYYY-MM-DD].[ext]
```

Examples:
- `requirements-v0.1-2026-05-04.md`
- `vibe-fingerprint-v0.1-2026-05-04.json`
- `gap-analysis-v0.1-2026-05-04.md`
- `stakeholder-map-v0.1-2026-05-04.json`
- `nfr-register-v0.1-2026-05-04.md`
- `risk-register-v0.1-2026-05-04.md`
- `spec-health-v0.1-2026-05-04.json`
