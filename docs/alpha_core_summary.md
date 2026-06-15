# Alpha Core Summary

Veyl Foundry Alpha Core is a local backend spine for building and evaluating
software-engineering agent environments.

The private Alpha Core has:

- a base of hand-authored Dockerized SWE tasks, extended with generated breadth
  and a growing set of **real human-sourced repository bug-fix tasks**;
- a public/private runtime split for solve and grade phases;
- hidden behavior grading, reproduced-environment grading for real tasks, and
  reference-equivalence (golden-output) grading;
- challenge probes that must fail;
- reference fixes that must pass;
- differential verification by a separate-provider solver, with every attempt
  captured and difficulty reported as a pass rate across repeated attempts;
- run persistence and replay;
- eval and training-environment export paths (one validated task serves both);
- domain packs that tag tasks by industry and failure area and render their own
  evidence from committed metadata;
- hardening checks for leakage and task quality.

This public mirror includes only a small runnable slice. It is not the private
task pack and not a hosted product.

## What The Public Mirror Proves

The mirror proves that the Foundry loop can be explained and used locally:

1. Load a task.
2. Copy its workspace into a run directory.
3. Execute visible public checks.
4. Persist a run log.
5. Replay the log.
6. Export a safe eval payload.

## What It Does Not Prove

The mirror does not prove broad benchmark quality, customer deployment, or
frontier-model performance. Those claims depend on private validation and
advisor-reviewed evidence.
