# Veyl Foundry Lite

**Veyl Foundry is an environment factory for software-engineering agent tasks** —
define a task, run an agent in a sandboxed workspace, grade its behavior against a
private oracle, replay the full run log, and export a safe evaluation artifact.
This repository is a small, runnable public slice of the system; the private
corpus, graders, and solutions stay private (see [Boundary](#boundary-public-vs-private)).

The bet behind Veyl: for coding agents, *writing a task is easy; proving the
grader is fair, deterministic, and un-gameable is the hard part.* Foundry is built
around that validation problem rather than around task generation.

## The loop

```
define task -> run agent in sandbox -> grade hidden behavior -> replay run log -> export eval / training artifact
```

Every task has a **public face** (a problem statement and a starting workspace) and
a **private oracle** (hidden behavioral checks, a reference fix that must pass, and
challenge probes that must fail). A task is only trusted after it survives a
multi-stage gate.

## The trust gate — why a task is believable

A candidate task is admitted to the corpus only if it passes *all* of:

- **Reference-fix passes / no-op fails.** The known-good fix makes the hidden
  checks pass; an empty change fails them. The task genuinely discriminates a real
  fix from nothing.
- **Challenge probes fail.** A battery of plausible-but-wrong and superficial
  patches must all be rejected, so the grader cannot be satisfied by reward-hacking
  instead of a real fix.
- **Zero-flake determinism.** Grading is reproducible run-to-run; a nondeterministic
  task is rejected, not papered over.
- **Differential verification.** An independent solver, sourced from a *separate*
  model provider, attempts the task from only the public problem statement and
  workspace. The task is trusted only if that independent attempt behaves the way
  the gate predicts. Solver and author are isolated, and provider separation keeps a
  single model's blind spots (or its own training data) from validating its own
  tasks. Every independent attempt is captured as a sanitized trajectory record, and
  difficulty is reported as a **pass rate across repeated independent attempts** —
  not a single lucky or unlucky run.
- **Promotion guard.** A task enters the committed corpus copy-only, after the full
  gate, with its verdict and provenance recorded — nothing is mutated in place.

These rules are enforced as explicit invariants — solver isolation, provider
separation, registry exclusion of un-gated material, a copy-only promotion guard,
bounded retries, and seed safety — and checked by a hardening pass that also scans
for answer or solution leakage into the public surface.

## Grading modes

Foundry grades a task in whichever way makes its outcome checkable and
deterministic:

- **Hidden behavioral checks** — the default: private checks the public workspace
  never sees.
- **Reproduced-environment grading** — for real repository tasks, the maintainers'
  own test suite, run in a pinned per-task environment so an old project grades
  exactly as it did upstream.
- **Reference-equivalence grading** — grade a system by deterministic
  output-equivalence against a reference implementation or a recorded golden output.
  This is the mechanism for grading a *specific workflow* against its own known-good
  result, on a deliberately deterministic domain.

## Real-task sourcing

Generated tasks are good for breadth and calibration. For *frontier* difficulty,
Foundry ingests **real repository bug-fix tasks**: a real broken commit, the
maintainers' hidden tests, and the human gold fix. The environment is reconstructed
on demand and graded with a pinned, per-task setup, then run through the same trust
gate. A real task is stored as a lightweight, provenance-tagged record that is at
once an **evaluation item** and a verifiable **training environment** — one artifact,
two uses. Sourcing is not limited to one public benchmark: any (repository,
problem, failing-test) triple — including a domain project pinned to a specific
broken commit — can be ingested through the same path.

**An honest finding from building this.** Across our trials, AI-*generated* tasks —
even carefully authored ones — did not stump a frontier model; real human-sourced
bugs did. Generation is bounded by the author's own competence. Frontier-hard,
trustworthy tasks come from *real sourcing plus rigorous validation*, not from
generation alone. That finding is exactly why the validation layer, not the
generator, sits at the center of the system.

**Measured, not asserted.** On a set of real human-sourced bugs, an independent
frontier model — given only the public problem statement — produced no passing fix
across repeated independent attempts on each, with every attempt captured and graded
in a pinned environment. Repeated-attempt measurement is also what keeps the claim
honest: it caught a task that looked frontier-hard on a single attempt but was solved
on others, and that task was re-labeled rather than kept. Difficulty here is an
evidenced pass rate, not a one-shot anecdote.

## Domain packs

Validated tasks are tagged by industry and failure area and curated into **domain
packs**. A pack carries its own evidence — coverage by failure area, provenance, and
measured difficulty per task — rendered straight from the committed task metadata
(a number appears only if it travels with the task). The first pack targets fintech:
payment idempotency under retries and partial completion, billing-replay determinism,
monetary arithmetic, and bank-identifier validation — including a real fintech bug an
independent frontier model failed to fix from the public problem alone. The packs and
their tasks are private; this mirror documents the shape.

## Quickstart: fail, then pass

The starter sample is intentionally incomplete. This command succeeds when the
starter *fails* the public checks — i.e., Foundry Lite correctly catches a broken
implementation:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --expect-fail
```

Then run the public-only passing implementation:

```bash
python3 -m foundry_lite run --task examples/pipeline-replay-public --use-public-solution
```

Export a public eval artifact, then replay the latest log:

```bash
python3 -m foundry_lite export --task examples/pipeline-replay-public --output out/pipeline_replay_eval.json
python3 -m foundry_lite replay --run out/latest
```

Passing this simplified public sample does **not** imply passing Veyl's private
evaluations.

## Boundary — public vs private

This repository is generated by an **explicit allowlist** plus a safety scan that
fails the build if any private marker leaks. It deliberately **excludes** the full
private task corpus, all private grading material, reference and challenge solutions,
full model run logs, provider command templates, and any internal strategy material.
The private repository is canonical; this is a derived artifact — a runnable proof
of *shape*, not a hosted product and not a benchmark-quality claim.
