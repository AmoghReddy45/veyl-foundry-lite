from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("FOUNDRY_WORKSPACE", ROOT / "workspace")).resolve()
CLI = WORKSPACE / "pipeline_replay.py"
FIXTURES = ROOT / "fixtures"
EXPECTED = FIXTURES / "expected"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


class PublicPipelineReplayTest(unittest.TestCase):
    def run_cli(self, root: Path, input_names: tuple[str, ...], output_name: str) -> Path:
        output = root / output_name
        cmd = [sys.executable, str(CLI)]
        for name in input_names:
            cmd.extend(["--input", str(FIXTURES / name)])
        cmd.extend(["--output", str(output)])
        result = subprocess.run(cmd, cwd=WORKSPACE, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        return output

    def test_public_outputs_match_expected_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.run_cli(
                Path(tmp),
                ("stream_public_a.ndjson", "stream_public_b.ndjson"),
                "out",
            )
            for name in ("ledger.jsonl", "invoice.jsonl", "audit.jsonl"):
                with self.subTest(name=name):
                    self.assertEqual(
                        (output / name).read_text(encoding="utf-8"),
                        (EXPECTED / name).read_text(encoding="utf-8"),
                    )

    def test_replay_is_stable_when_input_order_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self.run_cli(root, ("stream_public_a.ndjson", "stream_public_b.ndjson"), "first")
            reversed_order = self.run_cli(root, ("stream_public_b.ndjson", "stream_public_a.ndjson"), "reversed")
            for name in ("ledger.jsonl", "invoice.jsonl", "audit.jsonl"):
                with self.subTest(name=name):
                    self.assertEqual(
                        (first / name).read_text(encoding="utf-8"),
                        (reversed_order / name).read_text(encoding="utf-8"),
                    )

    def test_invoice_totals_match_ledger_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.run_cli(
                Path(tmp),
                ("stream_public_a.ndjson", "stream_public_b.ndjson"),
                "out",
            )
            ledger = read_jsonl(output / "ledger.jsonl")
            invoices = read_jsonl(output / "invoice.jsonl")
            for invoice in invoices:
                key = (invoice["account_id"], invoice["bill_date"])
                lines = [row for row in ledger if (row["account_id"], row["bill_date"]) == key]
                self.assertEqual(invoice["line_count"], len(lines))
                self.assertEqual(invoice["subtotal_cents"], sum(row["gross_cents"] for row in lines))


if __name__ == "__main__":
    unittest.main()
