from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schema import PublicTask


@dataclass(frozen=True)
class LiteRunResult:
    run_dir: Path
    passed: bool
    expected_failure: bool
    events: list[dict[str, Any]]


def run_task(
    task: PublicTask,
    output: str | Path,
    *,
    command: str | None = None,
    expect_fail: bool = False,
) -> LiteRunResult:
    run_dir = Path(output).resolve()
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    workspace = run_dir / "workspace"
    shutil.copytree(task.workspace_dir, workspace)

    events: list[dict[str, Any]] = []
    add_event(events, "run.start", task_id=task.task_id, workspace=str(workspace))

    env = os.environ.copy()
    env["FOUNDRY_WORKSPACE"] = str(workspace)
    env["VEYL_PUBLIC_TASK_ROOT"] = str(task.root)

    if command:
        add_event(events, "command.start", command=command)
        command_result = subprocess.run(
            command,
            cwd=workspace,
            shell=True,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        add_event(
            events,
            "command.finish",
            returncode=command_result.returncode,
            passed=command_result.returncode == 0,
        )

    check_results = []
    for check in task.public_checks:
        add_event(events, "check.start", command=check)
        result = subprocess.run(
            check,
            cwd=task.root,
            shell=True,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        check_results.append(result.returncode == 0)
        add_event(
            events,
            "check.finish",
            command=check,
            returncode=result.returncode,
            passed=result.returncode == 0,
            stdout_tail=tail(result.stdout),
            stderr_tail=tail(result.stderr),
        )

    passed = all(check_results)
    add_event(events, "run.finish", passed=passed, expected_failure=expect_fail)
    write_run_log(run_dir, task, passed, expect_fail, events)
    latest = run_dir.parent / "latest"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(run_dir, target_is_directory=True)
    return LiteRunResult(run_dir=run_dir, passed=passed, expected_failure=expect_fail, events=events)


def add_event(events: list[dict[str, Any]], event_type: str, **fields: Any) -> None:
    events.append({"ts": now(), "type": event_type, **fields})


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_run_log(
    run_dir: Path,
    task: PublicTask,
    passed: bool,
    expect_fail: bool,
    events: list[dict[str, Any]],
) -> None:
    payload = {
        "task_id": task.task_id,
        "passed": passed,
        "expected_failure": expect_fail,
        "events": events,
    }
    (run_dir / "run_log.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tail(value: str, limit: int = 1200) -> str:
    if len(value) <= limit:
        return value
    return value[-limit:]


def replay(run_dir: str | Path) -> str:
    path = Path(run_dir).resolve() / "run_log.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    lines = [f"task={payload['task_id']} passed={payload['passed']} expected_failure={payload['expected_failure']}"]
    for event in payload["events"]:
        detail = " ".join(f"{key}={value!r}" for key, value in event.items() if key not in {"ts", "type"})
        lines.append(f"{event['ts']} {event['type']} {detail}".rstrip())
    return "\n".join(lines) + "\n"
