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

## Quickstart: fail, then pass

The starter sample is intentionally incomplete. This command succeeds when the
starter fails the public checks, which demonstrates Foundry Lite catching an
incorrect implementation:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --expect-fail
```

Then run the public-only passing implementation:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --use-public-solution
```

That second command demonstrates Foundry Lite recognizing a correct repair for
the simplified public sample. Passing this public sample does not imply passing
Veyl's private evaluations.

After repairing the sample workspace yourself, run:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public
```

Export a public eval artifact:

```bash
python3 -m foundry_lite export --task examples/pipeline-replay-public --output out/pipeline_replay_eval.json
```

Replay the latest log:

```bash
python3 -m foundry_lite replay --run out/latest
```

## Boundary

This mirror demonstrates the shape of Foundry. The valuable private assets stay
in the private repo: the full task pack, private grading material, challenge
probes, model attempts, and advisor-only proof material.
