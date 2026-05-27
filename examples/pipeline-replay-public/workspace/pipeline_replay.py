"""Public starter for deterministic billing replay.

The implementation is intentionally incomplete. It behaves like an online
append-only processor, which is the class of bug the sample asks an agent to
repair.
"""

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


def event_type(event: dict[str, Any]) -> str:
    return str(event.get("type") or event.get("event_type") or "")


def event_time(event: dict[str, Any]) -> datetime:
    raw = event.get("occurred_at") or event.get("event_time") or event.get("arrived_at")
    return parse_timestamp(str(raw))


def event_units(event: dict[str, Any]) -> int:
    return int(event.get("units", 0))


def replay(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    current_plan_by_account: dict[str, str] = defaultdict(lambda: "starter")
    ledger_buckets: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []

    for event in events:
        kind = event_type(event)
        account_id = str(event.get("account_id", ""))
        if kind == "plan_change":
            current_plan_by_account[account_id] = str(event["plan"])
            audit_rows.append(
                {
                    "kind": "plan_change_applied",
                    "event_id": event["event_id"],
                    "account_id": account_id,
                    "effective_date": bill_day(parse_timestamp(str(event.get("effective_at") or event.get("occurred_at")))),
                    "plan": str(event["plan"]),
                }
            )
            continue
        if kind in {"correction", "tombstone"}:
            continue
        if kind != "usage":
            continue

        when = event_time(event)
        arrived_at = parse_timestamp(str(event.get("arrived_at") or event.get("received_at") or event.get("occurred_at")))
        service = str(event["service"])
        plan = current_plan_by_account[account_id]
        units = event_units(event)
        rate = PLAN_RATES_CENTS[plan].get(service, 0)
        key = (account_id, bill_day(when), service, plan)
        bucket = ledger_buckets.setdefault(
            key,
            {
                "account_id": account_id,
                "bill_date": bill_day(when),
                "service": service,
                "plan": plan,
                "units": 0,
                "gross_cents": 0,
                "events": [],
            },
        )
        bucket["units"] += units
        bucket["gross_cents"] += units * rate
        bucket["events"].append(str(event["event_id"]))

        if bill_day(arrived_at) > bill_day(when):
            audit_rows.append(
                {
                    "kind": "late_arrival",
                    "event_id": event["event_id"],
                    "bill_date": bill_day(when),
                    "arrival_date": bill_day(arrived_at),
                    "lag_days": (arrived_at.date() - when.date()).days,
                }
            )

    ledger_rows = sorted(ledger_buckets.values(), key=lambda row: (row["bill_date"], row["account_id"], row["service"], row["plan"]))
    invoice_buckets: dict[tuple[str, str], dict[str, Any]] = {}
    for row in ledger_rows:
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

    invoice_rows = sorted(invoice_buckets.values(), key=lambda row: (row["bill_date"], row["account_id"]))
    audit_rows.sort(key=lambda row: (row["kind"], row["event_id"]))
    return ledger_rows, invoice_rows, audit_rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def run(input_paths: list[Path], output_dir: Path) -> None:
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
    run(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
