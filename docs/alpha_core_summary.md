# Foundry background and current scope

Foundry Alpha Core was Veyl's early environment and evaluation infrastructure for
software-engineering tasks. Task authoring, behavior checks, repeated execution,
evidence storage, and export helped establish the evaluation discipline behind
the later reliability product.

Veyl's current product context is described in the
[product overview](product_overview.md). Earlier descriptions of task packs,
grading modes, or internal corpus size are historical context, not a feature
list for the code in this repository.

## What Foundry Lite implements

1. Load a `public-0.1` task definition.
2. Copy its workspace to a local output directory.
3. Optionally execute a command or apply the included public implementation.
4. Run the visible checks and record their results.
5. Display the saved event log.
6. Export public task metadata as an evaluation payload.

The public sample contains all its visible checks and fixtures. Private grading,
managed deployment, multi-provider experiments, and customer operating controls
are outside this package.

## How to evaluate the public material

Run the [quickstart](quickstart.md), inspect the
[sample contract](flagship_pipeline_replay_public.md), and read the separate
[published studies](public_evidence.md). A working local example is evidence of
the mechanics it implements, not a production deployment or a general claim
about model performance.
