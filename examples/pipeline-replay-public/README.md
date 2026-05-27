# Pipeline Replay Public Example

This example is a visible, runnable sample inspired by Veyl's internal
deterministic billing replay flagship.

The starter implementation is incomplete. It treats event streams as an online
append-only feed and misses important replay semantics.

Run the expected-failure check:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --expect-fail
```

Then repair:

```text
workspace/pipeline_replay.py
```

Run the passing check:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public
```
