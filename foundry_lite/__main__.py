from __future__ import annotations

import argparse
import sys
from .export import export_eval
from .runner import execute_task, replay
from .schema import load_task


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="foundry-lite")
    subparsers = parser.add_subparsers(dest="action", required=True)

    execute_parser = subparsers.add_parser("run")
    execute_parser.add_argument("--task", required=True)
    execute_parser.add_argument("--output", default="out/public-run")
    execute_parser.add_argument("--command", dest="agent_command")
    execute_parser.add_argument("--expect-fail", action="store_true")
    execute_parser.add_argument("--use-public-solution", action="store_true")

    replay_parser = subparsers.add_parser("replay")
    replay_parser.add_argument("--run", required=True)

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--task", required=True)
    export_parser.add_argument("--output", required=True)

    args = parser.parse_args(argv)
    if args.action == "run":
        task = load_task(args.task)
        result = execute_task(
            task,
            args.output,
            command=args.agent_command,
            expect_fail=args.expect_fail,
            use_public_solution=args.use_public_solution,
        )
        if args.expect_fail:
            if result.passed:
                print("Expected public checks to fail, but they passed.", file=sys.stderr)
                return 1
            print(f"Public checks failed as expected. Log: {result.session_dir / 'log.json'}")
            return 0
        if result.passed:
            print(f"Public checks passed. Log: {result.session_dir / 'log.json'}")
            return 0
        print(f"Public checks failed. Log: {result.session_dir / 'log.json'}", file=sys.stderr)
        return 1
    if args.action == "replay":
        print(replay(args.run), end="")
        return 0
    if args.action == "export":
        export_eval(load_task(args.task), args.output)
        print(f"Wrote {args.output}")
        return 0
    raise AssertionError(args.action)


if __name__ == "__main__":
    raise SystemExit(main())
