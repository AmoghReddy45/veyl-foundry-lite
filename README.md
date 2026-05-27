# Veyl Foundry Lite

Veyl Foundry is an environment factory for software-engineering agent tasks:
define a task, run a workspace, grade behavior, replay the run log, and export a
safe eval artifact.

This public mirror is a small runnable slice. It is meant to be useful, but it
does not contain the private task corpus, private grading material, solution
patches, probe patches, full run logs, provider command templates, or evaluator
operations.

## Included

- `foundry_lite`: a minimal local runner for public tasks.
- `examples/pipeline-replay-public`: a visible deterministic billing replay
  sample inspired by the internal flagship.
- Public docs describing the Alpha Core, security model, and private corpus
  boundary.

## Quickstart

The starter sample is intentionally incomplete. This command succeeds when the
starter fails the public checks:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --expect-fail
```

After repairing the sample workspace, run:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public
```

Export a public eval artifact:

```bash
python3 -m foundry_lite export --task examples/pipeline-replay-public --output out/pipeline_replay_eval.json
```

Replay the last run log:

```bash
python3 -m foundry_lite replay --run out/latest
```

## Boundary

This mirror demonstrates the shape of Foundry. The valuable private assets stay
in the private repo: the full task pack, private grading material, challenge
probes, model traces, and advisor-only proof material.
