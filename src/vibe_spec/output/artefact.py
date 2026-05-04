"""Artefact versioning and file management per CONSTITUTION Article 6."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def generate_run_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_output_dir(base: Path, run_id: str) -> Path:
    """Create versioned output directory: output/<run_id>-<YYYY-MM-DD>/"""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    dir_path = base / "output" / f"{run_id[:8]}-{date_str}"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def artefact_filename(artefact_type: str, version: str, date: str) -> str:
    """Generate canonical artefact filename per Article 6.5."""
    return f"{artefact_type}-v{version}-{date}.json"


def write_artefact(output_dir: Path, artefact_type: str, data: dict[str, Any], version: str = "0.1") -> Path:
    """Write an artefact JSON file to the output directory."""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = artefact_filename(artefact_type, version, date_str)
    path = output_dir / filename
    path.write_text(json.dumps(data, indent=2))
    return path


def append_approval_log(
    data: dict[str, Any],
    tier: int,
    reviewer: str,
    action: str,
    modification_note: str | None = None,
) -> dict[str, Any]:
    """Append a HITL approval record to an artefact per Article 6.2."""
    entry: dict[str, Any] = {
        "timestamp": now_iso(),
        "hitl_tier": tier,
        "reviewer": reviewer,
        "action": action,
    }
    if modification_note:
        entry["modification_note"] = modification_note

    if "approval_log" not in data:
        data["approval_log"] = []
    data["approval_log"].append(entry)
    return data
