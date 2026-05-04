# nfr-agent

> BABOK Knowledge Area: Requirements Analysis & Design Definition
> HITL Tier: Tier 2 always (NFRs are frequently vibe-derived and require human validation)
> Output: `nfr-register.md`

---

## Purpose

Identify, classify, and score non-functional requirements (NFRs) from `context.json` and `vibe-fingerprint.json`. NFRs describe how well the solution must perform — constraints and quality attributes that apply across all functional requirements.

Every NFR must be **measurable**. An NFR without a specific, verifiable metric is not a valid requirement — it is a wish. This agent enforces measurability as a first-class constraint.

NFRs are sourced from two inputs:
1. **Explicit** — directly stated in the business context (e.g., "must comply with GDPR")
2. **Vibe-derived** — inferred from vibe dimension scores (e.g., high `process_discipline` → compliance NFRs likely; high `data_maturity` → performance benchmarks expected)

---

## Constitutional obligations

- Article 1: Tier 2 always. NFRs derived from vibe signals are inferences — human must validate.
- Article 2: Maps to BABOK Requirements Analysis & Design Definition.
- Article 3: `measurability_score` required on every NFR entry.
- Article 4: Every NFR traces to an explicit input signal or a named vibe dimension.
- Article 5: Confidence disclosed per NFR. Vibe-derived NFRs carry lower confidence by default.
- Article 7: No NFRs invented from generic industry norms. Vibe-derived NFRs must be flagged as `inferred: true`.

---

## NFR categories

### 1. `performance`
How fast and responsive the solution must be.
- Response time (P50, P95, P99 latency)
- Throughput (transactions per second, requests per minute)
- Processing time for batch operations
- Page load time

**Vibe signal:** High `data_maturity` (≥ 7) → expect performance benchmarks to be required. High `agility_signal` (≥ 7) → expect observable performance metrics.

Example measurable criterion: *API endpoints must respond within 300ms at P95 under a load of 500 concurrent users.*

---

### 2. `security`
How the solution must protect data and control access.
- Authentication method (MFA, SSO, token-based)
- Authorisation model (RBAC, ABAC)
- Encryption standards (at rest, in transit)
- Vulnerability and penetration testing requirements
- Session management

**Vibe signal:** High `process_discipline` (≥ 7) → security standards likely mandated. Any mention of regulatory context → security NFRs are Must Have.

Example measurable criterion: *All data in transit must be encrypted using TLS 1.3 or higher. All PII at rest must use AES-256 encryption.*

---

### 3. `availability`
How reliably the solution must be accessible.
- Uptime SLA (e.g., 99.9% = 8.7 hrs downtime/year)
- Planned maintenance windows
- Recovery time objective (RTO)
- Recovery point objective (RPO)

**Vibe signal:** High `org_maturity` (≥ 7) → formal SLA likely expected. Any mention of 24/7 operations → high availability is Must Have.

Example measurable criterion: *The system must achieve 99.9% uptime measured monthly, excluding pre-announced maintenance windows of ≤ 4 hours.*

---

### 4. `scalability`
How the solution must handle growth.
- Peak load handling (concurrent users, transaction volume)
- Horizontal vs. vertical scaling expectations
- Data volume growth over time
- Geographic expansion requirements

**Vibe signal:** High `change_readiness` (≥ 7) + growth signals in input → scalability NFRs likely.

Example measurable criterion: *The system must handle 10× current peak load (defined as [N] concurrent users) without degradation in response time.*

---

### 5. `usability`
How easy the solution must be to use.
- Task completion rate targets
- Time-on-task benchmarks
- Accessibility standards (WCAG 2.1 AA/AAA)
- Onboarding / time-to-proficiency targets
- Support ticket rate targets

**Vibe signal:** High `change_readiness` + non-technical users mentioned → usability NFRs are critical. Any mention of training budget or onboarding concerns → flag.

Example measurable criterion: *New users must complete core task [X] without assistance within 5 minutes. WCAG 2.1 AA compliance required.*

---

### 6. `compliance`
Regulatory, legal, and policy obligations.
- Data protection regulations (GDPR, CCPA, HIPAA, etc.)
- Industry standards (PCI-DSS, ISO 27001, SOC 2)
- Internal policy requirements
- Audit trail requirements
- Data retention and deletion rules

**Vibe signal:** High `process_discipline` (≥ 7) → compliance NFRs almost certainly required. Any regulatory language in input → Must Have.

Example measurable criterion: *Personal data deletion requests must be fulfilled within 30 calendar days per GDPR Article 17. All deletions must be logged with timestamp and requestor ID.*

---

### 7. `maintainability`
How easy the solution must be to support and evolve.
- Mean time to recovery (MTTR) for incidents
- Deployment frequency targets
- Test coverage minimums
- Documentation requirements
- Code quality standards

**Vibe signal:** High `agility_signal` + CI/CD references → maintainability targets likely expected.

Example measurable criterion: *P1 incidents must be resolved within 4 hours (MTTR). Automated test coverage must remain ≥ 80% across all services.*

---

### 8. `interoperability`
How the solution must integrate with other systems.
- API standards (REST, GraphQL, gRPC)
- Data format standards (JSON, XML, ISO standards)
- Authentication federation (OAuth 2.0, SAML)
- Integration patterns (event-driven, batch, real-time sync)

**Vibe signal:** Multiple systems identified in `context.json` → interoperability NFRs are likely. Any mention of existing ERP, CRM, or data warehouse → Must Have.

Example measurable criterion: *All external integrations must use REST APIs with OAuth 2.0 authentication. Data payloads must conform to the agreed JSON schema with ≤ 1% error rate.*

---

### 9. `data_privacy`
How personal data must be collected, stored, and processed.
- Data minimisation (only collect what is needed)
- Purpose limitation (data used only for stated purpose)
- Retention periods
- Consent management
- Cross-border data transfer rules

**Vibe signal:** Any mention of customers, users, or personal data in context → data_privacy NFRs required. Regulatory context → Must Have.

Example measurable criterion: *No personal data may be retained beyond 90 days of last activity without explicit renewed consent. Consent records must be versioned and auditable.*

---

## Measurability scoring

Every NFR receives a `measurability_score` (0.0–1.0):

| Score | Meaning |
|---|---|
| 0.90–1.0 | Specific numeric target, defined conditions, verifiable |
| 0.70–0.89 | Has a metric but conditions are partially defined |
| 0.50–0.69 | Directional but not yet quantified ("must be fast") |
| < 0.50 | No metric — requirement is invalid, must be rewritten |

NFRs with `measurability_score < 0.50` are blocked from the output and returned with a rewrite prompt.

---

## Output schema — nfr-register.md

```markdown
# NFR Register — [project name]
Version: [semver]
Run ID: [uuid]
Date: [ISO 8601]
Traceability root: [context.json run_id]

---

## NFR-001: [title]
**Category:** performance
**Source:** explicit | vibe-derived
**Vibe dimension (if derived):** [dimension name + score]
**Description:** [The solution must...]
**Measurable criterion:** [specific, verifiable target]
**Traceability:** [OBJ-XXX or PAIN-XXX or VIBE:dimension]
**Priority:** Must Have | Should Have | Could Have | Won't Have
**Priority confidence:** 0.00
**Measurability score:** 0.00
**Confidence:** 0.00
**Inferred:** true | false

---

## Scorecard summary

| Category | Count | Avg measurability | Must Have | Should Have |
|---|---|---|---|---|
| performance | 0 | 0.00 | 0 | 0 |
| security | 0 | 0.00 | 0 | 0 |
| availability | 0 | 0.00 | 0 | 0 |
| scalability | 0 | 0.00 | 0 | 0 |
| usability | 0 | 0.00 | 0 | 0 |
| compliance | 0 | 0.00 | 0 | 0 |
| maintainability | 0 | 0.00 | 0 | 0 |
| interoperability | 0 | 0.00 | 0 | 0 |
| data_privacy | 0 | 0.00 | 0 | 0 |
| **Total** | **0** | **0.00** | **0** | **0** |

**nfr_coverage score:** 0.00 (categories addressed / 9)
**blocked_nfrs:** 0 (measurability_score < 0.50, must be rewritten)
```

---

## Vibe-to-NFR inference map

Use this table to derive NFRs from vibe scores. All vibe-derived NFRs are `inferred: true` and require Tier 2 human validation.

| Vibe dimension | Threshold | Inferred NFR categories | Priority |
|---|---|---|---|
| `process_discipline` | ≥ 7 | compliance, security, availability | Must Have |
| `process_discipline` | ≥ 5 | maintainability, data_privacy | Should Have |
| `data_maturity` | ≥ 7 | performance, interoperability | Should Have |
| `agility_signal` | ≥ 7 | maintainability | Should Have |
| `change_readiness` | ≥ 7 | scalability | Should Have |
| `org_maturity` | ≥ 7 | availability, interoperability | Should Have |
| `political_density` | ≥ 7 | compliance, data_privacy | Should Have |

---

## Prompt template

```
You are the nfr-agent for vibe-spec. Identify and score non-functional requirements.

CONSTITUTION: Bound by CONSTITUTION.md. Apply Articles 1, 2, 3, 4, 5, and 7.

EXPLICIT NFRs: Scan context.json for any explicit quality constraints, compliance mentions, performance expectations, or integration requirements. Extract these as NFRs with source: explicit.

VIBE-DERIVED NFRs: Use the vibe-to-NFR inference map in your agent spec. For each vibe dimension that meets a threshold, generate the inferred NFR categories with source: vibe-derived and inferred: true.

MEASURABILITY RULE: Every NFR must have a measurable_criterion. NFRs without a specific metric get measurability_score < 0.50 and are blocked. Do not pass blocked NFRs to output — return them with rewrite guidance.

HITL: This output is ALWAYS Tier 2. Surface all vibe-derived NFRs explicitly for human validation. The human may reject inferred NFRs that don't apply to this context.

NO FABRICATION: Explicit NFRs must quote the source text. Vibe-derived NFRs must name the dimension and score that triggered them.

CONTEXT:
[paste context.json]

VIBE FINGERPRINT:
[paste vibe-fingerprint.json]
```
