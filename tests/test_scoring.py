"""Tests for scoring modules."""

import pytest
from vibe_spec.scoring.invest import detect_ambiguity, score_story
from vibe_spec.scoring.spec_health import SpecHealthInput, compute_spec_health


class TestInvestScoring:
    def test_clean_story_passes(self) -> None:
        invest, ambiguity = score_story(
            story_text="As a user, I want to reset my password, so that I can regain access to my account.",
            acceptance_criteria=[
                "AC1: User receives reset email within 60 seconds",
                "AC2: Reset link expires after 1 hour",
            ],
        )
        assert invest.average >= 0.75
        assert ambiguity.flag_count == 0

    def test_weasel_word_flagged(self) -> None:
        _, ambiguity = score_story(
            story_text="As a user, I want an intuitive and seamless experience.",
            acceptance_criteria=["AC1: User completes task"],
        )
        assert ambiguity.flag_count >= 2

    def test_single_ac_fails_testable(self) -> None:
        invest, _ = score_story(
            story_text="As a user, I want to log in, so that I can access my dashboard.",
            acceptance_criteria=["AC1: User can log in"],
        )
        assert invest.testable < 1.0


class TestSpecHealth:
    def test_release_ready(self) -> None:
        result = compute_spec_health(
            SpecHealthInput(
                requirements_completeness=0.90,
                gap_coverage=0.85,
                stakeholder_completeness=0.80,
                vibe_confidence_avg=0.85,
                risk_coverage=0.80,
            )
        )
        assert result.status == "release_ready"
        assert result.score >= 0.80

    def test_elicitation_required(self) -> None:
        result = compute_spec_health(
            SpecHealthInput(
                requirements_completeness=0.40,
                gap_coverage=0.30,
                stakeholder_completeness=0.40,
                vibe_confidence_avg=0.50,
                risk_coverage=0.30,
            )
        )
        assert result.status == "elicitation_required"
        assert result.score < 0.60

    def test_invalid_input_raises(self) -> None:
        with pytest.raises(ValueError):
            SpecHealthInput(
                requirements_completeness=1.5,
                gap_coverage=0.80,
                stakeholder_completeness=0.80,
                vibe_confidence_avg=0.80,
                risk_coverage=0.80,
            )
