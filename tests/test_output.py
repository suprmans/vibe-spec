"""Tests for artefact output management."""

import json
from pathlib import Path

from vibe_spec.output.artefact import (
    append_approval_log,
    artefact_filename,
    generate_run_id,
    now_iso,
    write_artefact,
)


class TestArtefactFilename:
    def test_format(self) -> None:
        name = artefact_filename("requirements", "0.1", "2026-05-04")
        assert name == "requirements-v0.1-2026-05-04.json"

    def test_different_types(self) -> None:
        assert (
            artefact_filename("risk-register", "0.2", "2026-01-01")
            == "risk-register-v0.2-2026-01-01.json"
        )


class TestGenerateRunId:
    def test_is_uuid_format(self) -> None:
        run_id = generate_run_id()
        assert len(run_id) == 36
        assert run_id.count("-") == 4

    def test_unique(self) -> None:
        assert generate_run_id() != generate_run_id()


class TestNowIso:
    def test_is_iso_format(self) -> None:
        ts = now_iso()
        assert "T" in ts
        assert "+" in ts or "Z" in ts or ts.endswith("+00:00")


class TestWriteArtefact:
    def test_writes_json_file(self, tmp_path: Path) -> None:
        data = {"run_id": "abc", "type": "context"}
        path = write_artefact(tmp_path, "context", data, version="0.1")
        assert path.exists()
        written = json.loads(path.read_text())
        assert written["run_id"] == "abc"

    def test_filename_follows_convention(self, tmp_path: Path) -> None:
        path = write_artefact(tmp_path, "requirements", {}, version="0.2")
        assert "requirements-v0.2-" in path.name
        assert path.suffix == ".json"


class TestApprovalLog:
    def test_adds_entry(self) -> None:
        data: dict[str, object] = {"run_id": "abc"}
        result = append_approval_log(data, tier=2, reviewer="analyst", action="approved")
        log = result.get("approval_log")
        assert isinstance(log, list)
        assert len(log) == 1
        entry = log[0]
        assert isinstance(entry, dict)
        assert entry["hitl_tier"] == 2
        assert entry["reviewer"] == "analyst"
        assert entry["action"] == "approved"

    def test_appends_to_existing_log(self) -> None:
        data: dict[str, object] = {"approval_log": [{"existing": True}]}
        result = append_approval_log(
            data, tier=3, reviewer="ba", action="modified", modification_note="Revised scope"
        )
        log = result.get("approval_log")
        assert isinstance(log, list)
        assert len(log) == 2
        assert log[1].get("modification_note") == "Revised scope"

    def test_modification_note_only_when_provided(self) -> None:
        data: dict[str, object] = {}
        result = append_approval_log(data, tier=1, reviewer="auto", action="approved")
        log = result.get("approval_log")
        assert isinstance(log, list)
        assert "modification_note" not in log[0]
