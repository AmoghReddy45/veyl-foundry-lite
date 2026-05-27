# Alpha Core Summary

Veyl Foundry Alpha Core is a local backend spine for building and evaluating
software-engineering agent environments.

The private Alpha Core has:

- 34 Dockerized SWE tasks;
- a public/private runtime split for solve and grade phases;
- hidden behavior grading;
- challenge probes that must fail;
- reference fixes that must pass;
- run persistence and replay;
- eval and SFT export paths;
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
