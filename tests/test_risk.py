"""Tests for risk scoring module."""

import pytest

from vibe_spec.scoring.risk import (
    compute_risk_coverage,
    compute_risk_register_scorecard,
    compute_risk_score,
)


class TestRiskScore:
    def test_critical_risk(self) -> None:
        result = compute_risk_score(9.0, 9.0)
        assert result.classification == "critical"
        assert result.risk_score == 8.1
        assert result.is_critical

    def test_high_risk(self) -> None:
        result = compute_risk_score(7.0, 7.0)
        assert result.classification == "high"

    def test_medium_risk(self) -> None:
        result = compute_risk_score(4.0, 5.0)
        assert result.classification == "medium"

    def test_low_risk(self) -> None:
        result = compute_risk_score(1.0, 1.0)
        assert result.classification == "low"
        assert not result.is_critical

    def test_boundary_critical(self) -> None:
        result = compute_risk_score(7.0, 10.0)
        assert result.risk_score == 7.0
        assert result.classification == "critical"

    def test_invalid_likelihood_raises(self) -> None:
        with pytest.raises(ValueError, match="likelihood must be 0.0–10.0"):
            compute_risk_score(11.0, 5.0)

    def test_invalid_impact_raises(self) -> None:
        with pytest.raises(ValueError, match="impact must be 0.0–10.0"):
            compute_risk_score(5.0, -1.0)

    def test_zero_risk(self) -> None:
        result = compute_risk_score(0.0, 0.0)
        assert result.risk_score == 0.0
        assert result.classification == "low"


class TestRiskCoverage:
    def test_full_coverage(self) -> None:
        all_cats = [
            "requirements",
            "technical",
            "stakeholder",
            "compliance",
            "delivery",
            "data",
            "political",
        ]
        assert compute_risk_coverage(all_cats) == 1.0

    def test_partial_coverage(self) -> None:
        assert compute_risk_coverage(["requirements", "technical"]) == round(2 / 7, 4)

    def test_duplicates_not_double_counted(self) -> None:
        assert compute_risk_coverage(["requirements", "requirements", "technical"]) == round(
            2 / 7, 4
        )

    def test_empty_coverage(self) -> None:
        assert compute_risk_coverage([]) == 0.0


class TestRiskRegisterScorecard:
    def test_scorecard_counts_correctly(self) -> None:
        risks = [
            {
                "classification": "critical",
                "category": "requirements",
                "mitigation_confidence": 0.8,
            },
            {"classification": "high", "category": "technical", "mitigation_confidence": 0.5},
            {"classification": "medium", "category": "stakeholder", "mitigation_confidence": 0.7},
        ]
        scorecard = compute_risk_register_scorecard(risks)
        assert scorecard["total_risks"] == 3
        counts = scorecard["by_classification"]
        assert isinstance(counts, dict)
        assert counts["critical"] == 1
        assert counts["high"] == 1
        assert counts["medium"] == 1
        assert scorecard["low_confidence_mitigations"] == 1

    def test_empty_register(self) -> None:
        scorecard = compute_risk_register_scorecard([])
        assert scorecard["total_risks"] == 0
        assert scorecard["avg_mitigation_confidence"] == 0.0
