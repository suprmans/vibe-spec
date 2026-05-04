"""Risk scoring — likelihood × impact matrix."""

from dataclasses import dataclass

RISK_CATEGORIES = frozenset(
    {
        "requirements",
        "technical",
        "stakeholder",
        "compliance",
        "delivery",
        "data",
        "political",
    }
)

THRESHOLD_CRITICAL = 7.0
THRESHOLD_HIGH = 4.0
THRESHOLD_MEDIUM = 2.0


@dataclass
class RiskScore:
    likelihood: float
    impact: float
    risk_score: float
    classification: str

    @property
    def is_critical(self) -> bool:
        return self.classification == "critical"


def compute_risk_score(likelihood: float, impact: float) -> RiskScore:
    """Compute risk score and classification from likelihood and impact."""
    if not (0.0 <= likelihood <= 10.0):
        raise ValueError(f"likelihood must be 0.0–10.0, got {likelihood}")
    if not (0.0 <= impact <= 10.0):
        raise ValueError(f"impact must be 0.0–10.0, got {impact}")

    score = round(likelihood * impact / 10, 4)

    if score >= THRESHOLD_CRITICAL:
        classification = "critical"
    elif score >= THRESHOLD_HIGH:
        classification = "high"
    elif score >= THRESHOLD_MEDIUM:
        classification = "medium"
    else:
        classification = "low"

    return RiskScore(
        likelihood=likelihood,
        impact=impact,
        risk_score=score,
        classification=classification,
    )


def compute_risk_coverage(categories_present: list[str]) -> float:
    """Fraction of 7 risk categories covered in the register."""
    valid = {c for c in categories_present if c in RISK_CATEGORIES}
    return round(len(valid) / len(RISK_CATEGORIES), 4)


def compute_risk_register_scorecard(
    risks: list[dict[str, object]],
) -> dict[str, object]:
    """Compute summary scorecard for a full risk register."""
    counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    categories: list[str] = []
    mitigation_confidences: list[float] = []

    for risk in risks:
        classification = str(risk.get("classification", "low"))
        if classification in counts:
            counts[classification] += 1

        category = str(risk.get("category", ""))
        if category:
            categories.append(category)

        mc = risk.get("mitigation_confidence")
        if isinstance(mc, int | float):
            mitigation_confidences.append(float(mc))

    avg_mc = (
        round(sum(mitigation_confidences) / len(mitigation_confidences), 4)
        if mitigation_confidences
        else 0.0
    )
    low_confidence = sum(1 for mc in mitigation_confidences if mc < 0.60)

    return {
        "total_risks": len(risks),
        "by_classification": counts,
        "risk_coverage": compute_risk_coverage(categories),
        "avg_mitigation_confidence": avg_mc,
        "low_confidence_mitigations": low_confidence,
    }
