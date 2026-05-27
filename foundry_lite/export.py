from __future__ import annotations

import json
from pathlib import Path

from .schema import PublicTask


def export_eval(task: PublicTask, output: str | Path) -> None:
    payload = {
        "format": "eval",
        "schema_version": "public-0.1",
        "task": {
            "id": task.task_id,
            "prompt": task.prompt,
            "workspace": task.workspace,
            "public_check_count": len(task.public_checks),
            "metadata": task.metadata,
        },
    }
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
