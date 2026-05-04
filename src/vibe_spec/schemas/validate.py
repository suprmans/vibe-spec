"""Artefact schema validation against CONSTITUTION.md rules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMAS_DIR = Path(__file__).parent / "definitions"

_REQUIRED_FIELDS: dict[str, list[str]] = {
    "context": ["run_id", "timestamp", "babok_area", "intake_confidence", "entities"],
    "vibe_fingerprint": [
        "run_id",
        "timestamp",
        "babok_area",
        "vibe_dimensions",
        "vibe_confidence_avg",
        "ba_archetype",
        "hitl_tier",
    ],
    "nfr_register": ["run_id", "timestamp", "babok_area", "nfrs", "scorecard"],
}

_VIBE_DIMENSIONS = [
    "org_maturity",
    "agility_signal",
    "political_density",
    "process_discipline",
    "change_readiness",
    "data_maturity",
]


class ValidationError(Exception):
    pass


def validate_context(data: dict[str, Any]) -> list[str]:
    """Return list of constitutional violations in context.json."""
    violations = []
    for field in _REQUIRED_FIELDS["context"]:
        if field not in data:
            violations.append(f"Article 3: missing required field '{field}'")

    confidence = data.get("intake_confidence")
    if confidence is not None and not (0.0 <= confidence <= 1.0):
        violations.append("Article 5: intake_confidence must be 0.0–1.0")

    return violations


def validate_vibe_fingerprint(data: dict[str, Any]) -> list[str]:
    """Return list of constitutional violations in vibe-fingerprint.json."""
    violations = []
    for field in _REQUIRED_FIELDS["vibe_fingerprint"]:
        if field not in data:
            violations.append(f"Article 3: missing required field '{field}'")

    dimensions = data.get("vibe_dimensions", {})
    for dim in _VIBE_DIMENSIONS:
        if dim not in dimensions:
            violations.append(f"Article 3: missing vibe dimension '{dim}'")
            continue
        d = dimensions[dim]
        if "score" not in d or "confidence" not in d:
            violations.append(f"Article 3: dimension '{dim}' missing score or confidence")
        if "signals" not in d or len(d.get("signals", [])) < 1:
            violations.append(f"Article 7: dimension '{dim}' has no signals — possible fabrication")

    hitl = data.get("hitl_tier")
    if str(hitl) != "2":
        violations.append("Article 1: vibe_fingerprint hitl_tier must always be '2'")

    return violations


def validate_artefact(artefact_type: str, data: dict[str, Any]) -> list[str]:
    """Validate an artefact dict and return all constitutional violations."""
    validators = {
        "context": validate_context,
        "vibe_fingerprint": validate_vibe_fingerprint,
    }
    validator = validators.get(artefact_type)
    if validator is None:
        return [f"Unknown artefact type: {artefact_type}"]
    return validator(data)


def validate_file(artefact_type: str, path: Path) -> list[str]:
    """Load and validate a JSON artefact file."""
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    return validate_artefact(artefact_type, data)
