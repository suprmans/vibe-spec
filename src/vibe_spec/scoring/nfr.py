"""NFR measurability scoring."""

from dataclasses import dataclass

NFR_CATEGORIES = frozenset(
    {
        "performance",
        "security",
        "availability",
        "scalability",
        "usability",
        "compliance",
        "maintainability",
        "interoperability",
        "data_privacy",
    }
)

_METRIC_SIGNALS = [
    "ms",
    "millisecond",
    "second",
    "minute",
    "hour",
    "%",
    "percent",
    "percentage",
    "mb",
    "gb",
    "tb",
    "requests per",
    "transactions per",
    "per second",
    "per minute",
    "concurrent",
    "users",
    "uptime",
    "downtime",
    "days",
    "weeks",
    "months",
    "≤",
    "≥",
    ">=",
    "<=",
    "<",
    ">",
    "within",
    "at least",
    "no more than",
    "minimum",
    "maximum",
    "p95",
    "p99",
    "p50",
]

_VAGUE_SIGNALS = [
    "fast",
    "quickly",
    "slow",
    "responsive",
    "secure",
    "safely",
    "reliable",
    "stable",
    "easy",
    "simple",
    "intuitive",
    "appropriate",
    "adequate",
    "sufficient",
    "as needed",
    "when required",
]


@dataclass
class NfrMeasurabilityResult:
    score: float
    passes: bool
    blocked: bool
    metric_signals_found: list[str]
    vague_signals_found: list[str]
    feedback: str


def score_nfr_measurability(category: str, criterion: str) -> NfrMeasurabilityResult:
    """Score how measurable an NFR criterion is."""
    lower = criterion.lower()

    metric_signals = [s for s in _METRIC_SIGNALS if s in lower]
    vague_signals = [s for s in _VAGUE_SIGNALS if s in lower]

    metric_count = len(metric_signals)
    vague_count = len(vague_signals)

    if metric_count >= 3:
        score = min(1.0, 0.85 + (metric_count - 3) * 0.05)
    elif metric_count == 2:
        score = 0.80
    elif metric_count == 1:
        score = 0.65
    else:
        score = max(0.0, 0.40 - vague_count * 0.10)

    score = max(0.0, score - vague_count * 0.05)

    blocked = score < 0.50

    if blocked:
        feedback = (
            f"NFR blocked — measurability_score {score:.2f} < 0.50. "
            f"Add specific, verifiable metrics (e.g. thresholds, percentages, time bounds). "
            f"Vague terms to replace: {vague_signals or 'none found — add quantitative target'}."
        )
    elif score < 0.80:
        feedback = (
            f"NFR flagged for review — measurability_score {score:.2f}. "
            f"Consider adding more specific conditions (e.g. load level, percentile, time window)."
        )
    else:
        feedback = f"NFR passes measurability check — score {score:.2f}."

    return NfrMeasurabilityResult(
        score=round(score, 4),
        passes=score >= 0.50,
        blocked=blocked,
        metric_signals_found=metric_signals,
        vague_signals_found=vague_signals,
        feedback=feedback,
    )


def compute_nfr_coverage(categories_present: list[str]) -> float:
    """Fraction of the 9 NFR categories covered."""
    valid = {c for c in categories_present if c in NFR_CATEGORIES}
    return round(len(valid) / len(NFR_CATEGORIES), 4)
