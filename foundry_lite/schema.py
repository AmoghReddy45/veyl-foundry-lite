from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PublicTask:
    root: Path
    task_id: str
    prompt: str
    workspace: str
    public_checks: tuple[str, ...]
    metadata: dict[str, Any]

    @property
    def workspace_dir(self) -> Path:
        return self.root / self.workspace


def load_task(path: str | Path) -> PublicTask:
    root = Path(path).resolve()
    task_file = root / "task.yaml" if root.is_dir() else root
    data = yaml.safe_load(task_file.read_text(encoding="utf-8")) or {}
    if data.get("schema_version") != "public-0.1":
        raise ValueError(f"{task_file} must use schema_version public-0.1")
    checks = data.get("public_checks") or []
    if not checks:
        raise ValueError(f"{task_file} must define public_checks")
    workspace = data.get("workspace") or "workspace"
    task_root = task_file.parent
    return PublicTask(
        root=task_root,
        task_id=str(data["id"]),
        prompt=str(data["task_prompt"]),
        workspace=str(workspace),
        public_checks=tuple(str(command) for command in checks),
        metadata=dict(data.get("metadata") or {}),
    )
