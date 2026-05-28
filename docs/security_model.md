# Security Model

This public mirror is generated through an explicit allowlist. The private repo
is canonical; the public mirror is a derived artifact.

Allowed export sources:

- `README.public.md`
- `pyproject.public.toml`
- `docs/public`
- `foundry_lite`
- `examples/pipeline-replay-public`
- `LICENSE` when present

The exporter scans the generated mirror for forbidden private markers and fails
if any are found.

## Excluded Material

The public mirror excludes:

- the full private task corpus;
- private grading material;
- private solution material;
- probe patches;
- full model logs;
- provider command templates;
- evaluator operations.

## Limitations

Foundry Lite is a local demonstration. It is not a hardened hosted sandbox and
not a customer deployment surface. Treat it as a runnable proof of shape, not as
production infrastructure.
