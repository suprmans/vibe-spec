"""Tests for NFR measurability scoring."""

from vibe_spec.scoring.nfr import compute_nfr_coverage, score_nfr_measurability


class TestNfrMeasurability:
    def test_highly_measurable_criterion_passes(self) -> None:
        result = score_nfr_measurability(
            "performance",
            "API endpoints must respond within 300ms at P95 under 500 concurrent users.",
        )
        assert result.score >= 0.80
        assert result.passes
        assert not result.blocked

    def test_vague_criterion_blocked(self) -> None:
        result = score_nfr_measurability("performance", "The system should be fast and responsive.")
        assert result.blocked
        assert result.score < 0.50

    def test_partial_criterion_flagged_not_blocked(self) -> None:
        result = score_nfr_measurability("availability", "System uptime must be at least 99.9%.")
        assert result.passes
        assert not result.blocked

    def test_compliance_criterion_with_specific_deadline(self) -> None:
        result = score_nfr_measurability(
            "compliance",
            "Personal data deletion requests must be fulfilled within 30 days per GDPR Article 17.",
        )
        assert result.passes

    def test_feedback_present(self) -> None:
        result = score_nfr_measurability("security", "The system must be secure.")
        assert len(result.feedback) > 0


class TestNfrCoverage:
    def test_full_coverage(self) -> None:
        all_categories = [
            "performance",
            "security",
            "availability",
            "scalability",
            "usability",
            "compliance",
            "maintainability",
            "interoperability",
            "data_privacy",
        ]
        assert compute_nfr_coverage(all_categories) == 1.0

    def test_partial_coverage(self) -> None:
        assert compute_nfr_coverage(["performance", "security", "availability"]) == round(3 / 9, 4)

    def test_invalid_categories_ignored(self) -> None:
        assert compute_nfr_coverage(["performance", "invented_category"]) == round(1 / 9, 4)

    def test_empty_coverage(self) -> None:
        assert compute_nfr_coverage([]) == 0.0
