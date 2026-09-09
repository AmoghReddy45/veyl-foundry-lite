# Foundry Lite quickstart

Use Python 3.11 or later and run the commands from the repository root. The
included example requires PyYAML; it does not require a model account or Docker.

```bash
git clone https://github.com/AmoghReddy45/veyl-foundry-lite.git
cd veyl-foundry-lite
python3 -m venv .venv
source .venv/bin/activate
python -m pip install 'PyYAML>=6.0'
```

## Observe a failure

```bash
python -m foundry_lite run --task examples/pipeline-replay-public --output out/starter --expect-fail
```

The starter is deliberately incomplete. `--expect-fail` returns exit code 0 when
the visible checks fail as expected. The log still records `passed: false`.

## Observe a passing implementation

```bash
python -m foundry_lite run --task examples/pipeline-replay-public --output out/passing --use-public-solution
```

This applies the included implementation to a copied workspace. It does not
modify `examples/pipeline-replay-public/workspace/pipeline_replay.py`.

Inspect each result:

```bash
python -m foundry_lite replay --run out/starter
python -m foundry_lite replay --run out/passing
```

`out/latest` points to the most recent run. Reusing an output directory replaces
that directory, so use a separate path for results you want to retain.

## Repair the starter yourself

Edit `examples/pipeline-replay-public/workspace/pipeline_replay.py`, then run
without the included implementation:

```bash
python -m foundry_lite run --task examples/pipeline-replay-public --output out/my-repair
```

Exit code 0 means the visible checks passed; exit code 1 means they failed.

## Export public task metadata

```bash
python -m foundry_lite export --task examples/pipeline-replay-public --output out/pipeline_replay_eval.json
```

The export contains the task ID, prompt, workspace name, visible-check count,
and metadata. It is not an archive of the workspace or a deployment credential.

Read the [execution boundary](security_model.md) before supplying your own code
or commands. Passing the example does not qualify an agent for customer work.
