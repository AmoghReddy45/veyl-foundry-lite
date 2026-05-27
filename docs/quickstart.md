# Quickstart

Run the public sample:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --expect-fail
```

That command should pass because the starter implementation is intentionally
incomplete and should fail the visible public checks.

To solve it, repair:

```text
examples/pipeline-replay-public/workspace/pipeline_replay.py
```

Then run:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public
```

Useful commands:

```bash
python3 -m foundry_lite export --task examples/pipeline-replay-public --output out/pipeline_replay_eval.json
python3 -m foundry_lite replay --run out/latest
```

The public checks validate deterministic replay behavior over visible sample
data. Passing this sample does not imply passing any private Veyl evaluation.
