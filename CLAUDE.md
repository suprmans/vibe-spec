# CLAUDE.md — vibe-spec Agent Gateway

> This is the Claude Code entry point for the vibe-spec framework.
> Read CONSTITUTION.md before running any agent. Every agent in this project is bound by it.

---

## What this project does

`vibe-spec` converts unstructured business context into structured, scored, BABOK-aligned specification artefacts. You are the AI engine. The human analyst is the authority. The CONSTITUTION is the rulebook.

Input: meeting notes, problem statements, process descriptions, stakeholder briefs, or any unstructured business context.

Output: `context.json`, `vibe-fingerprint.json`, `requirements.md`, `gap-analysis.md`, `stakeholder-map.json`, `risk-register.md`, and a `spec_health` composite score.

---

## Mandatory pre-flight

Before running any agent, confirm:

1. You have read `CONSTITUTION.md` in full.
2. You know which HITL tier applies to each output you are about to generate.
3. You have the raw input context from the user ready.

If any of these are missing, stop and ask the user before proceeding.

---

## Agent pipeline

Run agents in this order. Do not skip stages. Do not run a later agent without the output of its predecessors.

```
[intake-agent]         →  context.json
      ↓
[vibe-analyzer]        →  vibe-fingerprint.json
      ↓
[HITL GATE 1]          ←  Human confirms org context
      ↓
[requirements-agent]   →  requirements.md + scorecard.json    (parallel)
[nfr-agent]            →  nfr-register.md                      (parallel)
      ↓
[HITL GATE 2]          ←  Human reviews stories + NFRs together
      ↓
[gap-agent]            →  gap-analysis.md          (parallel)
[stakeholder-agent]    →  stakeholder-map.json      (parallel)
      ↓
[HITL GATE 3]          ←  Human validates strategic alignment
      ↓
[risk-agent]           →  risk-register.md
      ↓
[HITL GATE 4]          ←  Human final sign-off
      ↓
[spec_health computed]
      ↓
Artefacts committed to version control
```

---

## How to invoke agents

Each agent lives in `agents/[agent-name].md`. To run an agent, read its file and follow the prompt template it defines. Pass the required inputs as specified.

### Full pipeline (recommended)

```
/vibe-spec analyse "[paste your business context here]"
```

The orchestrator chains all agents automatically and surfaces HITL gates at the right moments.

### Individual agents

```
/vibe-spec intake "[raw input]"
/vibe-spec vibe "[raw input or context.json path]"
/vibe-spec requirements "[context.json path] [vibe-fingerprint.json path]"
/vibe-spec gap "[requirements.md path] [context.json path]"
/vibe-spec stakeholders "[requirements.md path] [context.json path]"
/vibe-spec risks "[all prior artefact paths]"
```

---

## HITL gate protocol

When you reach a HITL gate, stop the pipeline and present the current artefact to the human for review. Use the format in `templates/hitl-review.md`.

**Never proceed past a gate without explicit human confirmation.**

At each gate, the human has three options:
- `approve` — proceed with the artefact as-is
- `modify [instructions]` — revise the artefact per the human's instructions, then re-present
- `reject [reason]` — discard the artefact, return to the generating agent with feedback

Log the gate outcome before proceeding.

---

## Constitutional enforcement

You are bound by `CONSTITUTION.md`. Before emitting any artefact output:

- Check Article 1: Is the HITL tier correctly assigned and applied?
- Check Article 2: Does this output map to a BABOK v3 knowledge area?
- Check Article 3: Does this output carry a complete metric scorecard?
- Check Article 4: Does every entity trace to a source in `context.json`?
- Check Article 5: Is confidence disclosed for every score and classification?
- Check Article 6: Is the artefact ready for version-controlled commit with approval log?
- Check Article 7: Is every entity grounded in the provided input — no invented entities?

If any check fails, do not emit the output. Fix the violation or flag it to the human.

---

## Output file locations

All artefacts are written to the `output/` directory (created per analysis run):

```
output/
└── [run-id]-[YYYY-MM-DD]/
    ├── context.json
    ├── vibe-fingerprint.json
    ├── requirements-v0.1-[date].md
    ├── scorecard.json
    ├── gap-analysis-v0.1-[date].md
    ├── stakeholder-map-v0.1-[date].json
    ├── risk-register-v0.1-[date].md
    └── spec-health-v0.1-[date].json
```

---

## Skills available

| Skill | Command | What it does |
|---|---|---|
| `vibe-ba` | `/vibe-spec:vibe-ba` | Org vibe analysis (intake + vibe-analyzer) |
| `req-elicitation` | `/vibe-spec:req-elicitation` | Requirements from context |
| `gap-analysis` | `/vibe-spec:gap-analysis` | Structured gap analysis |

---

## Integration with ai-first-sdlc-practices

Artefacts produced by vibe-spec map directly to ai-first-sdlc-practices conventions:

- `requirements.md` → `docs/feature-proposals/XX-name.md`
- `stakeholder-map.json` → consumed by `sdlc-team-pm` agents
- `risk-register.md` → input to `code-review-specialist` and `verification-enforcer`

---

*Governed by CONSTITUTION.md. Licensed under AGPL-3.0.*
