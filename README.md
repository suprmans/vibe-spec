# vibe-spec

> AI-first business specification framework for Business Analysts, Product Owners, and Product Managers.

`vibe-spec` converts unstructured business context — meeting notes, problem statements, process descriptions, stakeholder briefs — into structured, scored, audit-ready specification artefacts. Every output carries a metric scorecard and passes through human-in-the-loop review gates.

```
Business context (raw input)
           ↓
    [ vibe-spec agents ]
           ↓
   requirements.md  ·  nfr-register.md  ·  gap-analysis.md
   stakeholder-map.json  ·  risk-register.md  ·  spec_health score
           ↓
    ai-first-sdlc-practices  (downstream)
           ↓
   Architecture → Code → Ship
```

---

## What it produces

| Artefact | What it contains |
|---|---|
| `context.json` | Parsed entities: people, systems, processes, objectives, pain points, constraints |
| `vibe-fingerprint.json` | 6-dimension org maturity profile with confidence scores |
| `requirements.md` | INVEST-scored user stories + functional requirements, traced to business objectives |
| `nfr-register.md` | Non-functional requirements across 9 categories with measurability scores |
| `gap-analysis.md` | AS-IS → TO-BE delta ranked by impact × effort |
| `stakeholder-map.json` | Influence/interest matrix with engagement risk and cadence |
| `risk-register.md` | Risk register with likelihood × impact scoring |
| `spec-health.json` | Composite quality score — release-ready when ≥ 0.80 |

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Claude Code (for running agents)

---

## Setup

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
make install-dev

# Install pre-commit hooks
make pre-commit-install
```

---

## How to use

### Full pipeline via Claude Code

Open this project in Claude Code. The `CLAUDE.md` file wires up the agents automatically.

```
/vibe-spec:vibe-ba "Paste your business context here"
```

This runs the first two agents (intake + vibe-analyzer), scores the org vibe, and pauses at HITL Gate 1 for your review before proceeding.

### Individual skills

```
# Step 1 — Parse input and analyse org vibe
/vibe-spec:vibe-ba "[raw business context]"

# Step 2 — Generate requirements + NFRs (after Gate 1 approval)
/vibe-spec:req-elicitation "[context.json path]" "[vibe-fingerprint.json path]"

# Step 3 — Gap analysis (after Gate 2 approval)
/vibe-spec:gap-analysis "[requirements.md path]" "[context.json path]"
```

### CLI tools (Python)

```bash
# Validate an artefact against CONSTITUTION rules
uv run vibe-spec validate context output/abc123-2026-05-04/context-v0.1-2026-05-04.json

# Compute spec_health score
uv run vibe-spec score \
  --requirements-completeness 0.85 \
  --gap-coverage 0.80 \
  --stakeholder-completeness 0.75 \
  --vibe-confidence-avg 0.82 \
  --risk-coverage 0.70
```

---

## Agent pipeline

```
[intake-agent]          → context.json
        ↓
[vibe-analyzer]         → vibe-fingerprint.json
        ↓
[HITL GATE 1]           ← Human confirms org context
        ↓
[requirements-agent]    → requirements.md + scorecard.json    ┐ parallel
[nfr-agent]             → nfr-register.md                     ┘
        ↓
[HITL GATE 2]           ← Human reviews stories + NFRs
        ↓
[gap-agent]             → gap-analysis.md                     ┐ parallel
[stakeholder-agent]     → stakeholder-map.json                ┘
        ↓
[HITL GATE 3]           ← Human validates strategic alignment
        ↓
[risk-agent]            → risk-register.md
        ↓
[HITL GATE 4]           ← Human final sign-off
        ↓
[spec_health computed]
        ↓
Artefacts committed to version control
```

Each HITL gate gives you three options: `approve`, `modify [instructions]`, or `reject [reason]`.

---

## Org vibe fingerprint

The `vibe-analyzer` scores 6 dimensions of your organisation from the input, calibrating all downstream agents to your org's maturity and culture:

| Dimension | Measures | Range |
|---|---|---|
| `org_maturity` | Process discipline and documentation culture | 0 (ad-hoc) → 10 (optimised) |
| `agility_signal` | Sprint cadence and change tolerance | 0 (waterfall) → 10 (agile) |
| `political_density` | Stakeholder complexity and power dynamics | 0 (aligned) → 10 (high friction) |
| `process_discipline` | Workflow rigour and compliance orientation | 0 (chaotic) → 10 (governance-heavy) |
| `change_readiness` | Appetite for transformation | 0 (change-averse) → 10 (change-hungry) |
| `data_maturity` | Evidence-based vs. intuition-led decisions | 0 (gut-driven) → 10 (data-driven) |

---

## Requirements quality metrics

Every user story is scored against:

| Metric | Target |
|---|---|
| `invest_score` | ≥ 0.75 |
| `ambiguity_flag` | 0 flags |
| `ac_coverage` | ≥ 2 ACs per story |
| `priority_confidence` | ≥ 0.70 |
| `traceability_link` | Required |

Every NFR is scored for:

| Metric | Target |
|---|---|
| `measurability_score` | ≥ 0.80 (NFRs below 0.50 are blocked) |
| `priority_confidence` | ≥ 0.70 |

---

## Spec health score

```
spec_health = (
  requirements_completeness  × 0.30  +
  gap_coverage               × 0.25  +
  stakeholder_completeness   × 0.20  +
  vibe_confidence_avg        × 0.15  +
  risk_coverage              × 0.10
)
```

| Score | Status |
|---|---|
| ≥ 0.80 | Release-ready |
| 0.60–0.79 | Human review recommended |
| < 0.60 | Additional elicitation required |

---

## Development

### First-time setup

```bash
make install-dev        # install all dependencies including dev tools
make pre-commit-install # wire pre-commit hooks into .git/ (run once)
```

### Daily commands

```bash
make format        # ruff formatter + autofix
make lint          # ruff linter
make typecheck     # mypy strict type check
make test          # pytest
make test-cov      # pytest + coverage report (html + terminal)
make pre-commit-run  # run all hooks against every file manually
```

### Recommended workflow

```bash
make format && make test  # before every commit
```

Pre-commit hooks fire automatically on `git commit` — no need to run them manually unless you want to check the whole codebase at once:
- ruff lint + format
- mypy type check
- JSON / YAML / TOML validation
- Blocks direct commits to `main`

---

## Project structure

```
vibe-spec/
├── CONSTITUTION.md          ← BA methodology rules (single source of truth)
├── CLAUDE.md                ← Agent gateway for Claude Code
├── agents/
│   ├── intake-agent.md      ← Parse and structure raw input
│   ├── vibe-analyzer.md     ← Org culture + maturity fingerprint
│   ├── requirements-agent.md← User stories + functional requirements
│   ├── nfr-agent.md         ← Non-functional requirements (9 categories)
│   ├── gap-agent.md         ← AS-IS → TO-BE delta  [v0.2]
│   ├── stakeholder-agent.md ← Influence/interest matrix  [v0.2]
│   ├── risk-agent.md        ← Risk register  [v0.3]
│   └── orchestrator.md      ← Full pipeline chain  [v0.3]
├── skills/
│   ├── vibe-ba/SKILL.md     ← Claude skill: intake + vibe analysis
│   ├── req-elicitation/     ← Claude skill: requirements  [v0.2]
│   └── gap-analysis/        ← Claude skill: gap analysis  [v0.2]
├── src/vibe_spec/
│   ├── scoring/
│   │   ├── invest.py        ← INVEST criteria + ambiguity detection
│   │   └── spec_health.py   ← Composite score computation
│   ├── schemas/
│   │   └── validate.py      ← Constitutional artefact validation
│   ├── output/
│   │   └── artefact.py      ← Versioned file writing + approval logging
│   └── cli/
│       └── main.py          ← CLI: validate, score
├── tests/
│   └── test_scoring.py
├── templates/
│   ├── spec-output.md       ← Standard artefact output format  [v0.2]
│   └── hitl-review.md       ← Human review prompt template  [v0.2]
├── registry.json            ← Skill registry
├── pyproject.toml
├── Makefile
└── .pre-commit-config.yaml
```

---

## Roadmap

### v0.1 — Foundation ✓
- [x] `CONSTITUTION.md`
- [x] `intake-agent`
- [x] `vibe-analyzer`
- [x] `requirements-agent` (user stories + functional requirements)
- [x] `nfr-agent` (9 NFR categories with measurability scoring)
- [x] `vibe-ba` skill
- [x] `registry.json`
- [x] Python package scaffold (scoring, validation, CLI, output)

### v0.2 — Core agents
- [ ] `gap-agent` — AS-IS → TO-BE delta
- [ ] `stakeholder-agent` — influence/interest matrix
- [ ] `req-elicitation` skill
- [ ] `gap-analysis` skill
- [ ] HITL gates 1–3 fully implemented
- [ ] `scorecard.json` schema finalised
- [ ] `templates/` — spec-output and hitl-review templates

### v0.3 — Complete pipeline
- [ ] `risk-agent` — risk register with confidence scores
- [ ] `orchestrator` — full pipeline chain
- [ ] `spec_health` composite scoring (end-to-end)
- [ ] HITL gate 4
- [ ] ai-first-sdlc-practices integration test

### v1.0 — Public release
- [ ] `sdlc-team-ba` plugin for ai-first-sdlc-practices marketplace
- [ ] ReqIQ web interface
- [ ] Documentation site
- [ ] Example artefacts from real use cases

---

## License

AGPL-3.0. Free for personal and internal use. Commercial SaaS use requires a separate license — see `COMMERCIAL.md`.
