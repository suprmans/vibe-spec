"""spec_health composite score computation."""

from dataclasses import dataclass


WEIGHTS = {
    "requirements_completeness": 0.30,
    "gap_coverage": 0.25,
    "stakeholder_completeness": 0.20,
    "vibe_confidence_avg": 0.15,
    "risk_coverage": 0.10,
}

THRESHOLD_READY = 0.80
THRESHOLD_REVIEW = 0.60


@dataclass
class SpecHealthInput:
    requirements_completeness: float
    gap_coverage: float
    stakeholder_completeness: float
    vibe_confidence_avg: float
    risk_coverage: float

    def __post_init__(self) -> None:
        for field_name, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field_name} must be between 0.0 and 1.0, got {value}")


@dataclass
class SpecHealthResult:
    score: float
    status: str
    component_scores: dict[str, float]
    weighted_contributions: dict[str, float]
    recommendation: str


def compute_spec_health(inputs: SpecHealthInput) -> SpecHealthResult:
    """Compute the spec_health composite score."""
    components = {
        "requirements_completeness": inputs.requirements_completeness,
        "gap_coverage": inputs.gap_coverage,
        "stakeholder_completeness": inputs.stakeholder_completeness,
        "vibe_confidence_avg": inputs.vibe_confidence_avg,
        "risk_coverage": inputs.risk_coverage,
    }

    weighted = {k: v * WEIGHTS[k] for k, v in components.items()}
    score = sum(weighted.values())

    if score >= THRESHOLD_READY:
        status = "release_ready"
        recommendation = "Artefact set is release-ready for downstream SDLC consumption."
    elif score >= THRESHOLD_REVIEW:
        status = "review_recommended"
        recommendation = "Human review recommended before downstream use. Address low-scoring components."
    else:
        status = "elicitation_required"
        recommendation = "Additional elicitation required. Do not proceed until spec_health ≥ 0.60."

    return SpecHealthResult(
        score=round(score, 4),
        status=status,
        component_scores=components,
        weighted_contributions={k: round(v, 4) for k, v in weighted.items()},
        recommendation=recommendation,
    )
