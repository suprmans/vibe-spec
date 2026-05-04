"""Tests for constitutional artefact validation."""

from vibe_spec.schemas.validate import validate_artefact


class TestContextValidation:
    def test_valid_context_passes(self) -> None:
        data = {
            "run_id": "abc-123",
            "timestamp": "2026-05-04T10:00:00Z",
            "babok_area": "Business Analysis Planning & Monitoring",
            "intake_confidence": 0.85,
            "entities": {},
        }
        assert validate_artefact("context", data) == []

    def test_missing_field_flagged(self) -> None:
        data = {"run_id": "abc-123", "timestamp": "2026-05-04T10:00:00Z"}
        violations = validate_artefact("context", data)
        assert any("babok_area" in v for v in violations)

    def test_invalid_confidence_flagged(self) -> None:
        data = {
            "run_id": "abc-123",
            "timestamp": "2026-05-04T10:00:00Z",
            "babok_area": "Business Analysis Planning & Monitoring",
            "intake_confidence": 1.5,
            "entities": {},
        }
        violations = validate_artefact("context", data)
        assert any("intake_confidence" in v for v in violations)


class TestVibeFingerprintValidation:
    def _valid_dimension(self) -> dict[str, object]:
        return {
            "score": 7.5,
            "confidence": 0.85,
            "signals": ["signal 1", "signal 2"],
            "interpretation": "High",
        }

    def test_valid_fingerprint_passes(self) -> None:
        dims = {
            d: self._valid_dimension()
            for d in [
                "org_maturity",
                "agility_signal",
                "political_density",
                "process_discipline",
                "change_readiness",
                "data_maturity",
            ]
        }
        data = {
            "run_id": "abc-123",
            "timestamp": "2026-05-04T10:00:00Z",
            "babok_area": "Strategy Analysis",
            "vibe_dimensions": dims,
            "vibe_confidence_avg": 0.85,
            "ba_archetype": {"type": "accelerator", "rationale": "High agility"},
            "hitl_tier": "2",
        }
        assert validate_artefact("vibe_fingerprint", data) == []

    def test_wrong_hitl_tier_flagged(self) -> None:
        dims = {
            d: self._valid_dimension()
            for d in [
                "org_maturity",
                "agility_signal",
                "political_density",
                "process_discipline",
                "change_readiness",
                "data_maturity",
            ]
        }
        data = {
            "run_id": "abc-123",
            "timestamp": "2026-05-04T10:00:00Z",
            "babok_area": "Strategy Analysis",
            "vibe_dimensions": dims,
            "vibe_confidence_avg": 0.85,
            "ba_archetype": {},
            "hitl_tier": "1",
        }
        violations = validate_artefact("vibe_fingerprint", data)
        assert any("hitl_tier" in v for v in violations)

    def test_missing_dimension_flagged(self) -> None:
        data = {
            "run_id": "abc-123",
            "timestamp": "2026-05-04T10:00:00Z",
            "babok_area": "Strategy Analysis",
            "vibe_dimensions": {"org_maturity": self._valid_dimension()},
            "vibe_confidence_avg": 0.80,
            "ba_archetype": {},
            "hitl_tier": "2",
        }
        violations = validate_artefact("vibe_fingerprint", data)
        assert any("agility_signal" in v for v in violations)

    def test_dimension_without_signals_flagged(self) -> None:
        dim = {"score": 7.5, "confidence": 0.85, "signals": [], "interpretation": "High"}
        dims = dict.fromkeys(
            [
                "org_maturity",
                "agility_signal",
                "political_density",
                "process_discipline",
                "change_readiness",
                "data_maturity",
            ],
            dim,
        )
        data = {
            "run_id": "abc-123",
            "timestamp": "2026-05-04T10:00:00Z",
            "babok_area": "Strategy Analysis",
            "vibe_dimensions": dims,
            "vibe_confidence_avg": 0.85,
            "ba_archetype": {},
            "hitl_tier": "2",
        }
        violations = validate_artefact("vibe_fingerprint", data)
        assert any("signals" in v for v in violations)
