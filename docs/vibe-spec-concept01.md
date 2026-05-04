# vibe-spec

> The AI-first business specification framework for Business Analysts, Product Owners, and Product Managers.

---

## What is vibe-spec?

`vibe-spec` is to Business Analysis what `vibe-coding` is to software engineering.

Where a developer using vibe-coding describes intent and AI generates runnable code, a BA/PO/PM using vibe-spec describes a business situation — a problem statement, meeting transcript, process description, or stakeholder brief — and AI generates structured, audit-ready specification artefacts: requirements, gap analysis, stakeholder maps, org vibe fingerprints, and risk registers.

The **specification** is the deliverable. The **analyst** is the authority. The **AI** is the engine.

> "AI accelerates synthesis, but business analysts still determine what *usable* looks like."
> — IIBA, *How AI Enhances Business Analysis Without Replacing Professional Judgment*, 2026

---

## The analogy

| Role | Domain artifact | AI-first equivalent |
|---|---|---|
| Software engineer | Source code | vibe-coding (Karpathy, 2025) |
| Data analyst | Analytical report | vibe-analysis |
| Business Analyst / PO / PM | **Specification** | **vibe-spec** ← this project |

`vibe-spec` is the upstream layer that feeds AI-first SDLC frameworks (e.g., `ai-first-sdlc-practices`). It produces the feature proposals, requirements docs, and stakeholder context that developer workflows need but cannot generate themselves.

```
Business reality / problem statement
           ↓
    [ vibe-spec agents ]        ← this project
           ↓
   Structured spec artefacts
   (requirements, gap, vibe, stakeholders, risks)
           ↓
    ai-first-sdlc-practices     ← downstream consumer
           ↓
   Architecture → Code → Ship
```

---

## Framework foundations

`vibe-spec` is grounded in three established frameworks, combined into a single coherent methodology.

### 1. BABOK® v3 — Knowledge area alignment (IIBA)

The *Business Analysis Body of Knowledge* (BABOK® Guide, IIBA) is the globally recognised standard for BA practice. `vibe-spec` maps its agents directly to BABOK's six knowledge areas:

| BABOK® Knowledge area | vibe-spec agent | Primary output |
|---|---|---|
| Business Analysis Planning & Monitoring | `intake-agent` | Context JSON, scope definition |
| Elicitation & Collaboration | `elicitation-agent` | Structured themes from raw input |
| Requirements Life Cycle Management | `requirements-agent` | User stories, ACs, traceability matrix |
| Strategy Analysis | `vibe-analyzer` | Org vibe fingerprint, maturity score |
| Requirements Analysis & Design | `gap-agent` | AS-IS → TO-BE delta, prioritised gaps |
| Solution Evaluation | `risk-agent` | Risk register, confidence scores |

The BA's professional judgment governs all six areas. AI accelerates synthesis within each; it does not replace the analyst's accountability for accuracy, completeness, or strategic alignment.

### 2. NIST AI Risk Management Framework — Governance model

The NIST AI RMF (NIST, 2023) defines four interconnected functions for responsible AI deployment: **GOVERN → MAP → MEASURE → MANAGE**. vibe-spec adopts this structure as its operational governance layer.

```
GOVERN   Define BA standards, output quality thresholds,
         human review triggers, and escalation rules.
         → CONSTITUTION.md in every vibe-spec project

MAP      Identify the business context, stakeholders,
         and what the AI system is being asked to analyse.
         → intake-agent + vibe-analyzer

MEASURE  Employ quantitative, qualitative, and mixed-method
         scoring to assess and benchmark analysis outputs.
         → Qualitative Metric Scorecard (see §4 below)

MANAGE   Human-in-the-loop review, approval gates,
         artefact versioning, and continuous improvement.
         → Human Review Protocol (see §3 below)
```

> "Measuring AI risks includes tracking metrics for trustworthy characteristics, social impact, and human-AI configurations."
> — NIST AI RMF Core, airc.nist.gov

### 3. Human-in-the-Loop (HITL) — Decision architecture

NIST AI RMF standards recommend human oversight for high-risk AI use cases — and business specifications are high-stakes by nature. A poorly formed requirement costs $1 to fix at specification time and $40–100 to fix in maintenance.

`vibe-spec` implements HITL at **three tiers**, matched to output confidence and business impact:

```
Tier 1 — Auto-pass (confidence ≥ 0.85, low-stakes dimensions)
  AI output is accepted and logged. Human may review asynchronously.
  Example: Non-functional requirement templates, standard AC patterns.

Tier 2 — Guided review (confidence 0.60–0.84, or medium-stakes)
  AI surfaces the output with a structured review prompt.
  Human confirms, modifies, or rejects each item explicitly.
  Example: Stakeholder classification, gap priority ranking.

Tier 3 — Human-first (confidence < 0.60, or high-stakes dimensions)
  AI drafts, but human must rewrite or explicitly approve before logging.
  Example: Org vibe fingerprint in politically sensitive contexts,
           requirements affecting compliance or regulation.
```

**HITL checkpoints in the workflow:**

```
Input received
      ↓
[AI] Intake parsing                     → auto-pass if well-formed
      ↓
[AI] Vibe analysis                      → Tier 2 review always
      ↓
[HUMAN] Confirm org context             ← GATE 1
      ↓
[AI] Requirements generation            → Tier 1/2 by confidence
      ↓
[HUMAN] Story review + AC sign-off      ← GATE 2
      ↓
[AI] Gap analysis + stakeholder map     → Tier 2 review
      ↓
[HUMAN] Strategic alignment check       ← GATE 3
      ↓
[AI] Risk register draft                → Tier 3 always
      ↓
[HUMAN] Final artefact approval         ← GATE 4 (sign-off)
      ↓
Artefacts committed to version control
```

The human is not a bottleneck — they are the quality gate. AI is an assistant, not an authority. Accountability for accuracy, governance, and decision-making still rests with the analyst.

---

## Qualitative metric scorecard

The core contribution of `vibe-spec` is converting unstructured business context into **scored, traceable, qualitative artefacts**. Every agent output carries a metric scorecard. This is what makes vibe-spec outputs audit-ready and comparable across projects.

### Vibe fingerprint (org context analysis)

Six dimensions, each scored 0.0–10.0, derived from linguistic and structural signals in the input:

| Dimension | What it measures | Low (0–3) | High (7–10) |
|---|---|---|---|
| `org_maturity` | Process discipline and documentation culture | Ad-hoc, informal | Defined, optimised |
| `agility_signal` | Sprint cadence, iteration culture, change tolerance | Waterfall, rigid | Agile, experimental |
| `political_density` | Stakeholder complexity, competing power dynamics | Low friction | High friction |
| `process_discipline` | Workflow rigour and compliance orientation | Chaotic | Governance-heavy |
| `change_readiness` | Appetite for transformation vs. stability preference | Change-averse | Change-hungry |
| `data_maturity` | Evidence-based decision culture vs. intuition-led | Gut-driven | Data-driven |

Confidence score per dimension. Dimensions below 0.60 confidence trigger Tier 3 HITL review.

### Requirements quality metrics

Each generated user story carries:

| Metric | Description | Target |
|---|---|---|
| `invest_score` | INVEST criteria compliance (Independent, Negotiable, Valuable, Estimable, Small, Testable) | ≥ 0.75 |
| `ambiguity_flag` | Linguistic ambiguity detection (weasel words, passive voice, unmeasurable claims) | 0 flags |
| `ac_coverage` | Acceptance criteria completeness vs. story scope | ≥ 2 ACs per story |
| `priority_confidence` | MoSCoW classification confidence | ≥ 0.70 |
| `traceability_link` | Linked to business objective or pain point | Required |

### Gap analysis metrics

| Metric | Description |
|---|---|
| `impact_score` | Business value of closing the gap (0.0–10.0) |
| `effort_estimate` | Relative implementation effort (XS / S / M / L / XL) |
| `dependency_count` | Number of other gaps this one blocks or is blocked by |
| `quick_win_flag` | Impact ≥ 6.0 AND effort ≤ S → flagged as quick win |

### Stakeholder engagement metrics

Each identified stakeholder carries:

| Metric | Values |
|---|---|
| `influence_score` | 0.0–10.0 |
| `interest_score` | 0.0–10.0 |
| `quadrant` | `manage_closely` / `keep_satisfied` / `keep_informed` / `monitor` |
| `engagement_risk` | `low` / `medium` / `high` — risk of misalignment if not engaged |
| `communication_cadence` | Recommended touchpoint frequency |

### Overall spec health score

A composite score computed at the end of each analysis run:

```
spec_health = weighted_average(
  requirements_completeness  * 0.30,
  gap_coverage               * 0.25,
  stakeholder_completeness   * 0.20,
  vibe_confidence_avg        * 0.15,
  risk_coverage              * 0.10
)
```

`spec_health ≥ 0.80` → artefact is release-ready.
`spec_health 0.60–0.79` → human review recommended.
`spec_health < 0.60` → additional elicitation required before proceeding.

---

## Agent architecture

```
vibe-spec/
├── LICENSE                  ← AGPL-3.0 full text
├── CLA.md                   ← Contributor License Agreement (required before PRs)
├── COMMERCIAL.md            ← Commercial licensing terms for SaaS operators
├── CONSTITUTION.md          ← BA methodology rules (single source of truth)
├── CLAUDE.md                ← Agent gateway for Claude Code
├── agents/
│   ├── intake-agent.md      ← Parse and structure raw input
│   ├── vibe-analyzer.md     ← Org culture + maturity fingerprint
│   ├── requirements-agent.md← BABOK-aligned user stories + ACs
│   ├── gap-agent.md         ← AS-IS → TO-BE delta analysis
│   ├── stakeholder-agent.md ← Influence/interest matrix + engagement plan
│   ├── risk-agent.md        ← Risk register with confidence scores
│   └── orchestrator.md      ← Chain all agents, manage HITL gates
├── skills/
│   ├── vibe-ba/
│   │   └── SKILL.md         ← Claude skill: org vibe analysis
│   ├── req-elicitation/
│   │   └── SKILL.md         ← Claude skill: requirements from context
│   └── gap-analysis/
│       └── SKILL.md         ← Claude skill: structured gap analysis
├── templates/
│   ├── spec-output.md       ← Standard artefact output format
│   ├── hitl-review.md       ← Human review prompt template
│   └── scorecard.json       ← Metric scorecard schema
├── registry.json            ← Skill registry for distribution
└── README.md                ← This file
```

### CONSTITUTION.md — The BA methodology rules

Inspired by the `CONSTITUTION.md` pattern from `ai-first-sdlc-practices`. Contains:

- **Article 1 — Human authority**: AI generates, humans approve. No artefact is final until a human has reviewed it at the appropriate HITL tier.
- **Article 2 — BABOK alignment**: All outputs must map to a BABOK® v3 knowledge area.
- **Article 3 — Metric completeness**: Every output carries a full metric scorecard. Outputs without scores are invalid.
- **Article 4 — Traceability**: Every requirement traces to a business objective. Every gap traces to a requirement or pain point. No orphan artefacts.
- **Article 5 — Confidence disclosure**: Every AI-generated score or classification discloses its confidence level. Low-confidence outputs are flagged, never silently accepted.
- **Article 6 — Version control**: All artefacts are committed to version control with timestamped HITL approval records.
- **Article 7 — No fabrication**: AI must not invent stakeholders, requirements, or risks without evidence in the input. Hallucination is a critical failure.

---

## Workflow — end to end

```
User provides input context
(meeting notes / problem statement / process description / stakeholder brief)
      │
      ▼
[intake-agent]
  - Classify input type
  - Extract entities: people, systems, processes, dates, constraints
  - Output: context.json
      │
      ▼
[vibe-analyzer]
  - Score 6 org dimensions (0.0–10.0 each)
  - Classify BA archetype most suited to this org
  - Identify red flags for BA engagement
  - Output: vibe-fingerprint.json
      │
      ▼
[HITL GATE 1] ← Human confirms org context is accurate
      │
      ▼
[requirements-agent]
  - Generate user stories calibrated to org maturity (vibe score)
  - Apply INVEST criteria + ambiguity check
  - Assign MoSCoW priority with confidence score
  - Output: requirements.md + scorecard.json
      │
      ▼
[HITL GATE 2] ← Human reviews and approves each story
      │
      ▼
[gap-agent] + [stakeholder-agent] (parallel)
  - Gap: AS-IS → TO-BE delta, ranked by impact × effort
  - Stakeholder: influence/interest matrix + engagement plan
  - Output: gap-analysis.md + stakeholder-map.json
      │
      ▼
[HITL GATE 3] ← Human validates strategic alignment
      │
      ▼
[risk-agent]
  - Extract risks from full context + prior agent outputs
  - Classify by likelihood × impact
  - All outputs at Tier 3 HITL (high-stakes by definition)
  - Output: risk-register.md
      │
      ▼
[HITL GATE 4] ← Human sign-off on complete artefact set
      │
      ▼
[spec_health score computed]
      │
      ▼
Artefacts committed to version control
Ready for downstream SDLC consumption
```

---

## Integration with ai-first-sdlc-practices

`vibe-spec` output is designed to feed directly into the `ai-first-sdlc-practices` framework by SteveGJones. The two projects form a complete AI-native delivery pipeline:

| Layer | Project | Input | Output |
|---|---|---|---|
| Business specification | **vibe-spec** | Problem context | `requirements.md`, `gap-analysis.md`, `stakeholder-map.json` |
| SDLC enforcement | `ai-first-sdlc-practices` | Feature proposals | Architecture → Code → PR → Ship |

The `vibe-spec` artefacts map directly to `ai-first-sdlc-practices` conventions:

- `requirements.md` → `docs/feature-proposals/XX-name.md`
- `stakeholder-map.json` → consumed by `sdlc-team-pm` agents
- `risk-register.md` → input to `code-review-specialist` and `verification-enforcer`

To use both together:

```bash
# Install vibe-spec skills
/plugin marketplace add suprmans/vibe-spec

# Run BA analysis
/vibe-spec:analyse "describe your business problem here"

# Hand off to SDLC
/sdlc-core:new-feature 1 my-feature "$(cat requirements.md)"
```

---

## Why vibe-spec exists — the gap in numbers

47% of project failures are due to poor requirements, and 60% of software development rework costs stem from incorrect or incomplete requirements (Standish Group CHAOS Report; IBM Systems Sciences Institute).

AI-powered requirements tools report 40–60% time savings in the requirements gathering phase and can help identify up to 30% more requirements that would otherwise be missed.

The problem is not that AI cannot help with BA work. The problem is that no structured, agent-based, metric-driven framework exists for BA the way `ai-first-sdlc-practices` exists for engineering. `vibe-spec` is that framework.

---

## Roadmap

### v0.1 — Foundation (solo, ~4 weeks)
- [ ] `CONSTITUTION.md` — BA methodology rules
- [ ] `intake-agent` — context parsing
- [ ] `vibe-analyzer` — org fingerprint (6 dimensions)
- [ ] `vibe-ba` SKILL.md — distributable Claude skill
- [ ] `registry.json` — skill registry schema

### v0.2 — Core agents (~3 weeks)
- [ ] `requirements-agent` — INVEST-scored user stories
- [ ] `gap-agent` — AS-IS → TO-BE delta
- [ ] `stakeholder-agent` — influence/interest matrix
- [ ] HITL gates 1–3 implemented
- [ ] `scorecard.json` schema finalised

### v0.3 — Complete pipeline (~2 weeks)
- [ ] `risk-agent` — risk register with confidence scores
- [ ] `orchestrator` — full pipeline chain
- [ ] `spec_health` composite scoring
- [ ] HITL gate 4 (final sign-off)
- [ ] `ai-first-sdlc-practices` integration test

### v1.0 — Public release
- [ ] `sdlc-team-ba` plugin for `ai-first-sdlc-practices` marketplace
- [ ] ReqIQ web interface (powered by vibe-spec agents)
- [ ] Documentation site
- [ ] Example artefacts from 5 real use cases

---

## Contributing

`vibe-spec` dogfoods its own methodology. All feature proposals are written using vibe-spec artefacts before any code is written.

**Before your first pull request:** read and agree to `CLA.md`. This is required for all contributions. It takes two minutes and protects everyone involved.

**To contribute a new agent or skill:**
1. Write a feature proposal using the `spec-output.md` template
2. Pass it through the vibe-spec pipeline (at minimum: requirements + gap + stakeholder)
3. Achieve `spec_health ≥ 0.80` before submitting a PR
4. Include the full metric scorecard in your PR description

**To contribute to the CONSTITUTION:**
- All proposed rule changes require a human-authored rationale
- Must not conflict with BABOK® v3 principles
- Must maintain HITL guarantees — no change that removes a human gate will be accepted

---

## References

- IIBA. *A Guide to the Business Analysis Body of Knowledge (BABOK® Guide) v3.0*. International Institute of Business Analysis, 2015.
- IIBA. *How AI Enhances Business Analysis Without Replacing Professional Judgment*. iiba.org, March 2026.
- NIST. *AI Risk Management Framework (AI RMF 1.0)*. National Institute of Standards and Technology, 2023. airc.nist.gov
- Standish Group. *CHAOS Report*. Referenced via Eltegra AI, 2025.
- Karpathy, A. *"There's a new kind of coding I call vibe coding."* X (formerly Twitter), February 2, 2025.
- Jones, S. *ai-first-sdlc-practices*. GitHub, 2025. github.com/SteveGJones/ai-first-sdlc-practices
- Pendo. *The Vibe PM and the Evolution of Product Management*. pendo.io, July 2025.

---

## License

`vibe-spec` is licensed under **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### Why AGPL-3.0

AGPL-3.0 is the right choice for this project because of who uses it and who might exploit it.

Individual BAs, POs, and PMs running vibe-spec locally, in Claude projects, or internally within their organisation are **completely unaffected** — AGPL places no restrictions on personal or internal use. The license only activates when someone builds a multi-user product or service on top of vibe-spec and serves it to others over a network. In that case, they must publish their modifications under the same terms.

This design achieves two things simultaneously: it keeps the project genuinely open for the community that matters most (practitioners), while ensuring that any commercial SaaS operator who wants to keep their modifications private must negotiate a commercial license. That is the mechanism that funds continued development.

MIT and Apache-2.0 were considered and rejected. Both would allow any operator to take vibe-spec, rebrand it, ship it as a paid service, and contribute nothing back — in code, credits, or revenue. The history of open-source projects under permissive licenses (Elasticsearch, Redis, MongoDB) demonstrates this outcome reliably at scale.

### Open-core model

```
vibe-spec/   (AGPL-3.0)            ReqIQ/   (Commercial)
├── agents/                         ├── hosted web interface
├── skills/                         ├── multi-user SaaS
├── CONSTITUTION.md                 ├── enterprise agents
└── templates/                      └── API access tier
```

`vibe-spec` is the open framework. `ReqIQ` is the commercial product layer built on top of it. The framework being AGPL does not restrict the commercial product — the copyright holder may license their own code under any additional terms.

### Contributing and CLA

All contributors must agree to the **Contributor License Agreement (CLA)** before their pull requests are merged. The CLA grants the project maintainer the right to use contributions under the AGPL-3.0 terms and, where necessary, under a separate commercial license.

This is a practical requirement, not a philosophical one. Without a CLA, every contributor retains independent copyright over their changes, which would make it impossible to offer a commercial license to SaaS operators without tracking down every contributor for written permission. The CLA protects contributors' rights while keeping the project's licensing options intact.

The CLA does **not** transfer copyright ownership — contributors retain their copyright. It grants a licence to use, sublicense, and distribute the contribution as part of this project.

### Three files that define the licensing structure

```
LICENSE            ← Full AGPL-3.0 text
CLA.md             ← Contributor License Agreement
COMMERCIAL.md      ← Commercial licensing terms (contact for SaaS use)
```

### Commercial licensing

If you want to use vibe-spec as the basis of a hosted or managed service without open-sourcing your modifications, a commercial license is available. Contact: see `COMMERCIAL.md` or open an issue tagged `commercial-enquiry`.

See the [full AGPL-3.0 text](https://www.gnu.org/licenses/agpl-3.0.html) for complete terms.

---

*vibe-spec is not affiliated with IIBA or NIST. BABOK® is a registered trademark of the International Institute of Business Analysis.*
