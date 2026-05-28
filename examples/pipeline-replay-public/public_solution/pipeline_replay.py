"""Public-only solution for the visible pipeline replay sample."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLAN_RATES_CENTS = {
    "starter": {"api_call": 2, "storage_gb_day": 15, "seat_day": 120},
    "growth": {"api_call": 1, "storage_gb_day": 12, "seat_day": 90},
    "enterprise": {"api_call": 1, "storage_gb_day": 10, "seat_day": 70},
}


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def bill_day(value: datetime) -> str:
    return value.date().isoformat()


def load_events(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def stable_json(row: dict[str, Any]) -> str:
    return json.dumps(row, sort_keys=True, separators=(",", ":"))


def event_type(row: dict[str, Any]) -> str:
    return str(row.get("type") or row.get("event_type") or "")


def event_time(row: dict[str, Any]) -> datetime:
    raw = row.get("occurred_at") or row.get("event_time") or row.get("effective_at") or row.get("arrived_at")
    return parse_timestamp(str(raw))


def arrival_time(row: dict[str, Any]) -> datetime:
    raw = row.get("arrived_at") or row.get("received_at") or row.get("occurred_at") or row.get("event_time")
    return parse_timestamp(str(raw))


def event_units(row: dict[str, Any]) -> int:
    if "units" in row:
        return int(row["units"])
    return int(row.get("quantity", 0))


def correction_units(row: dict[str, Any]) -> int:
    if "corrected_units" in row:
        return int(row["corrected_units"])
    return int(row["corrected_quantity"])


def canonicalize(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    payloads: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        payloads[str(row["event_id"])].append(stable_json(row))

    chosen_rows: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for event_id, variants in sorted(payloads.items()):
        chosen_rows.append(json.loads(min(variants)))
        duplicate_count = len(variants) - 1
        if duplicate_count:
            audit.append({"duplicate_count": duplicate_count, "event_id": event_id, "kind": "duplicate_ignored"})
    return chosen_rows, audit


def plan_for(changes: list[dict[str, Any]], account_id: str, when: datetime) -> str:
    candidates = [row for row in changes if row["account_id"] == account_id and row["effective_at"] <= when]
    if not candidates:
        return "starter"
    return max(candidates, key=lambda row: (row["effective_at"], row["event_id"]))["plan"]


def replay(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    canonical_rows, audit = canonicalize(rows)
    usage: dict[str, dict[str, Any]] = {}
    corrections: list[dict[str, Any]] = []
    tombstones: list[dict[str, Any]] = []
    plan_changes: list[dict[str, Any]] = []

    for row in canonical_rows:
        kind = event_type(row)
        event_id = str(row["event_id"])
        if kind == "usage":
            usage[event_id] = {
                "account_id": str(row["account_id"]),
                "arrived_at": arrival_time(row),
                "event_id": event_id,
                "event_time": event_time(row),
                "service": str(row["service"]),
                "units": event_units(row),
            }
        elif kind == "correction":
            corrections.append(
                {
                    "event_id": event_id,
                    "target_event_id": str(row["target_event_id"]),
                    "to_units": correction_units(row),
                    "event_time": event_time(row),
                }
            )
        elif kind == "tombstone":
            tombstones.append(
                {
                    "event_id": event_id,
                    "target_event_id": str(row["target_event_id"]),
                    "event_time": event_time(row),
                }
            )
        elif kind == "plan_change":
            plan_changes.append(
                {
                    "account_id": str(row["account_id"]),
                    "effective_at": parse_timestamp(str(row.get("effective_at") or row.get("occurred_at") or row.get("event_time"))),
                    "event_id": event_id,
                    "plan": str(row["plan"]),
                }
            )

    tombstoned_targets = {row["target_event_id"] for row in tombstones}
    for row in sorted(corrections, key=lambda item: (item["event_time"], item["event_id"])):
        target_id = row["target_event_id"]
        if target_id not in usage:
            continue
        if target_id in tombstoned_targets:
            continue
        previous = usage[target_id]["units"]
        usage[target_id]["units"] = row["to_units"]
        audit.append(
            {
                "event_id": row["event_id"],
                "from_units": previous,
                "kind": "correction_applied",
                "target_event_id": target_id,
                "to_units": row["to_units"],
            }
        )

    for row in sorted(tombstones, key=lambda item: (item["event_time"], item["event_id"])):
        target_id = row["target_event_id"]
        if target_id in usage:
            usage.pop(target_id)
            audit.append({"event_id": row["event_id"], "kind": "tombstone_applied", "target_event_id": target_id})

    for row in sorted(plan_changes, key=lambda item: (item["effective_at"], item["account_id"], item["event_id"])):
        audit.append(
            {
                "account_id": row["account_id"],
                "effective_date": bill_day(row["effective_at"]),
                "event_id": row["event_id"],
                "kind": "plan_change_applied",
                "plan": row["plan"],
            }
        )

    ledger_buckets: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for row in sorted(usage.values(), key=lambda item: item["event_id"]):
        account_id = row["account_id"]
        service = row["service"]
        date = bill_day(row["event_time"])
        plan = plan_for(plan_changes, account_id, row["event_time"])
        rate = PLAN_RATES_CENTS[plan].get(service, 0)
        key = (account_id, date, service, plan)
        bucket = ledger_buckets.setdefault(
            key,
            {
                "account_id": account_id,
                "bill_date": date,
                "events": [],
                "gross_cents": 0,
                "plan": plan,
                "service": service,
                "units": 0,
            },
        )
        bucket["events"].append(row["event_id"])
        bucket["units"] += row["units"]
        bucket["gross_cents"] += row["units"] * rate
        if bill_day(row["arrived_at"]) > date:
            audit.append(
                {
                    "arrival_date": bill_day(row["arrived_at"]),
                    "bill_date": date,
                    "event_id": row["event_id"],
                    "kind": "late_arrival",
                    "lag_days": (row["arrived_at"].date() - row["event_time"].date()).days,
                }
            )

    ledger = sorted(ledger_buckets.values(), key=lambda row: (row["bill_date"], row["account_id"], row["service"], row["plan"]))
    invoice_buckets: dict[tuple[str, str], dict[str, Any]] = {}
    for row in ledger:
        key = (row["account_id"], row["bill_date"])
        invoice = invoice_buckets.setdefault(
            key,
            {
                "account_id": row["account_id"],
                "bill_date": row["bill_date"],
                "currency": "USD",
                "line_count": 0,
                "subtotal_cents": 0,
            },
        )
        invoice["line_count"] += 1
        invoice["subtotal_cents"] += row["gross_cents"]

    invoices = sorted(invoice_buckets.values(), key=lambda row: (row["bill_date"], row["account_id"]))
    audit.sort(key=lambda row: (row["kind"], row["event_id"]))
    return ledger, invoices, audit


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(stable_json(row) + "\n")


def execute(input_paths: list[Path], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger, invoices, audit = replay(load_events(input_paths))
    write_jsonl(output_dir / "ledger.jsonl", ledger)
    write_jsonl(output_dir / "invoice.jsonl", invoices)
    write_jsonl(output_dir / "audit.jsonl", audit)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    execute(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
