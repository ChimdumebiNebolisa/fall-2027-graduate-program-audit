from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .io import read_json, write_json

DEFAULT_PROGRESS = {
    "project": "fall-2027-graduate-program-audit",
    "current_phase": "foundation",
    "phases": {},
    "regions": {"us": "pending", "canada": "pending", "europe": "pending"},
    "counts": {},
    "known_failures": [],
}


def update_progress(path: str | Path, **changes: object) -> dict[str, object]:
    progress = dict(read_json(path, DEFAULT_PROGRESS) or DEFAULT_PROGRESS)
    progress.update(changes)
    progress["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(path, progress)
    return progress

