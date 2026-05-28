# Public Pipeline Replay Sample

The public sample is inspired by Veyl's internal flagship task family:
deterministic replay of billing event streams into ledger, invoice, and audit
artifacts.

The sample asks for behavior that is common in production billing and backfill
systems:

- merge multiple event streams;
- support two event schema shapes;
- ignore duplicate event IDs deterministically;
- apply plan changes by effective time;
- apply corrections to target usage;
- remove tombstoned usage;
- bill late arrivals by usage time;
- emit stable JSONL artifacts.

The starter code is deliberately incomplete. It trusts arrival order and misses
several state semantics. The public repo also includes a public-only passing
implementation so reviewers can see both sides of the loop:

```text
starter -> fails visible checks
public implementation -> passes visible checks
```

That makes the sample useful as a visible public challenge without disclosing
the private flagship checks.

## Why This Matters

Agent-generated code can look correct while missing production contracts. The
internal flagship demonstrated this contrast with private model attempts, while
this public sample keeps the details sanitized.

The public sample exposes a small version of that failure family so reviewers
can inspect and run the idea locally.
