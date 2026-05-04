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

`vibe-spec` is the upstream specification layer that feeds any AI-native SDLC pipeline. It produces the feature proposals, requirements docs, and stakeholder context that engineering workflows need but cannot generate themselves.

```
Business reality / problem statement
           ↓
    [ vibe-spec agents ]        ← this project
           ↓
   Structured spec artefacts
   (requirements, gap, vibe, stakeholders, risks)
           ↓
    downstream SDLC pipeline
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
│   ├── requirements-agent.md← User stories + functional requirements
│   ├── nfr-agent.md         ← Non-functional requirements (9 categories)
│   ├── gap-agent.md         ← AS-IS → TO-BE delta analysis
│   ├── stakeholder-agent.md ← Influence/interest matrix + engagement plan
│   ├── risk-agent.md        ← Risk register with confidence scores
│   └── orchestrator.md      ← Chain all agents, manage HITL gates
├── skills/
│   ├── vibe-ba/
│   │   └── SKILL.md         ← Claude skill: org vibe analysis
│   ├── req-elicitation/
│   │   └── SKILL.md         ← Claude skill: requirements + NFRs
│   └── gap-analysis/
│       └── SKILL.md         ← Claude skill: gap + stakeholder analysis
├── src/vibe_spec/           ← Python tool layer (invoked by agents via Bash)
│   ├── scoring/
│   │   ├── invest.py        ← INVEST criteria + ambiguity detection
│   │   ├── nfr.py           ← NFR measurability scoring
│   │   └── spec_health.py   ← Composite spec_health computation
│   ├── schemas/
│   │   └── validate.py      ← Constitutional artefact validation
│   ├── output/
│   │   └── artefact.py      ← Versioned file writing + approval logging
│   └── cli/
│       └── main.py          ← CLI entry point (vibe-spec <command>)
├── templates/
│   ├── spec-output.md       ← Standard artefact output format
│   ├── hitl-review.md       ← Human review prompt template
│   └── scorecard.json       ← Metric scorecard schema
├── registry.json            ← Skill registry for distribution
├── pyproject.toml           ← Python package (uv)
├── Makefile                 ← Dev commands
└── README.md
```

### CONSTITUTION.md — The BA methodology rules

A single source of truth that governs all agent behaviour. vibe-spec uses 7 articles specific to BA practice:

- **Article 1 — Human authority**: AI generates, humans approve. No artefact is final until a human has reviewed it at the appropriate HITL tier.
- **Article 2 — BABOK alignment**: All outputs must map to a BABOK v3 knowledge area.
- **Article 3 — Metric completeness**: Every output carries a full metric scorecard. Outputs without scores are invalid.
- **Article 4 — Traceability**: Every requirement traces to a business objective. Every gap traces to a requirement or pain point. No orphan artefacts.
- **Article 5 — Confidence disclosure**: Every AI-generated score or classification discloses its confidence level. Low-confidence outputs are flagged, never silently accepted.
- **Article 6 — Version control**: All artefacts are committed to version control with timestamped HITL approval records.
- **Article 7 — No fabrication**: AI must not invent stakeholders, requirements, or risks without evidence in the input. Hallucination is a critical failure.

### Python tool layer — the deterministic computation engine

**Python is not called via Anthropic SDK tool_use — it is invoked by Claude agents via Bash commands** inside skill instructions. This is the Claude Code native pattern. The division of responsibility is:

| Layer | Responsibility |
|---|---|
| Claude agents | Reasoning, language understanding, judgment, orchestration |
| Python (invoked via Bash) | Deterministic scoring, schema validation, artefact I/O, mathematics |

Agents call Python tools when they need exact, reproducible computation — not AI estimates:

```bash
# Agent calls this inside a skill to get exact INVEST scores
uv run vibe-spec score-story \
  --text "As a user..." \
  --ac "User receives email within 60s" \
  --ac "Link expires after 1 hour"
# → invest_score: 0.83, ambiguity_flags: 0, passes: true

# Agent calls this to validate an artefact before passing to HITL gate
uv run vibe-spec validate context output/run-id/context.json
# → PASS or list of constitutional violations

# Agent calls this after all artefacts are complete
uv run vibe-spec spec-health \
  --requirements-completeness 0.85 \
  --gap-coverage 0.80 \
  --stakeholder-completeness 0.75 \
  --vibe-confidence-avg 0.82 \
  --risk-coverage 0.70
# → spec_health: 0.79, status: review_recommended
```

Future Python tools can extend to statistical analysis (scipy correlation between vibe dimensions and requirement quality across runs), data pipeline processing, or any computation where determinism and testability matter.

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
[requirements-agent]                        (parallel)
  - Generate user stories calibrated to org maturity (vibe score)
  - Call: `vibe-spec score-story` → exact INVEST scores
  - Call: `vibe-spec detect-ambiguity` → flag weasel words
  - Assign MoSCoW priority with confidence score
  - Output: requirements.md + scorecard.json
[nfr-agent]                                 (parallel)
  - Identify explicit NFRs from context
  - Derive vibe-signal NFRs (9 categories)
  - Call: `vibe-spec score-nfr` → measurability scores
  - Block NFRs with measurability < 0.50
  - Output: nfr-register.md
      │
      ▼
[HITL GATE 2] ← Human reviews stories + NFRs together
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

## Downstream SDLC integration

`vibe-spec` is the upstream specification layer. It sits before any SDLC engineering pipeline and provides the structured, human-approved artefacts that engineering workflows need to build the right thing.

| Layer | What it does | Input | Output |
|---|---|---|---|
| Business specification | **vibe-spec** | Problem context | `requirements.md`, `nfr-register.md`, `gap-analysis.md`, `stakeholder-map.json`, `risk-register.md` |
| SDLC pipeline | Your engineering workflow | Approved artefacts | Architecture → Code → PR → Ship |

### Artefact handoff

After Gate 4 approval, vibe-spec artefacts feed directly into your engineering process:

- `requirements.md` → feature proposals for sprint planning
- `nfr-register.md` → quality gates for architecture and code review
- `stakeholder-map.json` → engagement plan for delivery leads
- `gap-analysis.md` → scope and prioritisation input
- `risk-register.md` → risk inputs for review and verification

### Using vibe-spec

```bash
# Install vibe-spec
/plugin marketplace add suprmans/vibe-spec

# Run full BA analysis
/vibe-spec:vibe-ba "describe your business problem here"

# After HITL gates 1–4 complete, hand artefacts to your engineering pipeline
```

---

## Why vibe-spec exists — the gap in numbers

47% of project failures are due to poor requirements, and 60% of software development rework costs stem from incorrect or incomplete requirements (Standish Group CHAOS Report; IBM Systems Sciences Institute).

AI-powered requirements tools report 40–60% time savings in the requirements gathering phase and can help identify up to 30% more requirements that would otherwise be missed.

The problem is not that AI cannot help with BA work. The problem is that no structured, agent-based, metric-driven framework exists for BA the way engineering SDLC frameworks exist for developers. `vibe-spec` is that framework.

---

## Roadmap

### v0.1 — Foundation ✓
- [x] `CONSTITUTION.md` — BA methodology rules (7 articles)
- [x] `CLAUDE.md` — agent gateway for Claude Code
- [x] `intake-agent` — context parsing, entity extraction
- [x] `vibe-analyzer` — org fingerprint (6 dimensions, BA archetypes, red flags)
- [x] `requirements-agent` — user stories (INVEST-scored) + functional requirements
- [x] `nfr-agent` — non-functional requirements (9 categories, measurability scoring)
- [x] `vibe-ba` SKILL.md — distributable Claude skill
- [x] `registry.json` — skill registry schema
- [x] Python package scaffold (`scoring/`, `schemas/`, `output/`, `cli/`)
- [x] `pyproject.toml` + `Makefile` + `.pre-commit-config.yaml` (uv + ruff + mypy + pytest)

### v0.2 — Core agents ✓
- [x] `gap-agent` — AS-IS → TO-BE delta, 4-tier prioritisation matrix
- [x] `stakeholder-agent` — influence/interest matrix, engagement risk, red flags
- [x] `req-elicitation` SKILL.md — chains requirements-agent + nfr-agent + HITL Gate 2
- [x] `gap-analysis` SKILL.md — chains gap-agent + stakeholder-agent + HITL Gate 3
- [x] `templates/scorecard.json` — full JSON schema for all artefact scorecards
- [x] `templates/spec-output.md` + `templates/hitl-review.md`
- [x] Python CLI: `score-story`, `score-nfr`, `score-gap`, `spec-health`, `validate` — bash-callable with `--json` flag
- [x] `scoring/nfr.py` — measurability scoring engine
- [x] Test suite: 22 tests across scoring, validation modules (51% coverage)
- [x] Architecture: Claude Code native patterns (Bash-invoked Python, not SDK tool_use)

### v0.3 — Complete pipeline ✓
- [x] `risk-agent` — risk register, likelihood × impact matrix, 7 categories, Tier 3 always
- [x] `orchestrator` — full pipeline chain, constitutional validation at every stage, Gate 4
- [x] HITL Gate 4 with full artefact manifest and traceability chain validation
- [x] `spec_health` end-to-end via `vibe-spec spec-health --json` CLI
- [x] CLI: `score-risk`, `write-artefact` bash-callable commands added
- [x] `scoring/risk.py` — risk scoring engine with register scorecard
- [x] Test suite expanded: risk, output, and validation modules covered

### v1.0 — Public release
- [ ] `vibe-spec-ba` plugin for Claude Code plugin marketplace
- [ ] ReqIQ web interface (powered by vibe-spec agents)
- [ ] Documentation site
- [ ] Example artefacts from 5 real use cases
- [ ] `registry.json` hosted and resolvable via `/plugin marketplace add suprmans/vibe-spec`

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
