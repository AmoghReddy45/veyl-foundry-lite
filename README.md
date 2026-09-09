# Veyl

**Reliable autonomous systems for work that matters.**

Veyl evaluates and improves the complete agent deployment around a real workflow:
the model, instructions, knowledge, tools, permissions, environment, and human
handoff. The operating decision is specific to that work: **delegate, supervise,
or stop**. Relevant changes trigger revalidation.

This repository is Veyl's public product guide and **Foundry Lite**, a small,
runnable Python example of the evaluation loop. The managed platform and its
private evaluation system are developed separately.

[Website](https://veyl.work) · [How Veyl works](https://veyl.work/methodology) ·
[Public research](https://veyl.work/evidence) · [Contact](mailto:amogh@veyl.work)

## Explore Veyl

| Area | Focus | Learn more |
| --- | --- | --- |
| Agent reliability | Test an exact deployment, improve recurring failures, and establish when human review is required. | [Product overview](docs/product_overview.md) |
| Coding agents | Use engineering history and business rules to evaluate which changes still need an engineer. | [Coding-agent evaluation](https://veyl.work/coding-agent-evaluation) |
| Veyl Private | Scope models, company knowledge, agents, controls, and evaluation inside an approved infrastructure boundary. | [Private AI](https://veyl.work/private-ai) |
| Veyl Physical | Define and qualify physical missions, beginning with autonomous drone inspection. | [Physical AI](https://veyl.work/physical) |
| Research | Inspect independent public-repository studies and their limits. | [Evidence guide](docs/public_evidence.md) |

The published evidence currently centers on coding workflows. Product pages
describe the broader direction and engagement scope; this repository does not
ship enterprise deployment integrations, a private-AI appliance, or drone software.

## Run Foundry Lite

Requires **Python 3.11 or later**. From a fresh checkout:

```bash
git clone https://github.com/AmoghReddy45/veyl-foundry-lite.git
cd veyl-foundry-lite
python3 -m venv .venv
source .venv/bin/activate
python -m pip install 'PyYAML>=6.0'
```

The billing-replay starter deliberately fails the visible checks. This command
returns success when that expected failure is observed:

```bash
python -m foundry_lite run --task examples/pipeline-replay-public --expect-fail
```

Run the included passing implementation, then inspect and export the result:

```bash
python -m foundry_lite run --task examples/pipeline-replay-public --use-public-solution
python -m foundry_lite replay --run out/latest
python -m foundry_lite export --task examples/pipeline-replay-public --output out/pipeline_replay_eval.json
```

The passing implementation is applied to the copied run workspace. Your starter
file remains unchanged. Both runs use the same default output directory; use
`--output out/starter` and `--output out/passing` to retain both results.

Lite executes commands locally with your user's permissions. Use trusted sample
code; it provides no isolation from your machine. No model account, hosted
service, or Docker runtime is required for the included example.

## What is included

- `foundry_lite/`: task loading, local execution, visible checks, event replay,
  and public evaluation metadata export.
- `examples/pipeline-replay-public/`: an incomplete billing-replay implementation,
  visible fixtures and checks, and a public passing implementation.
- `docs/`: product context, research links, setup, and the public/private boundary.

Passing this example demonstrates the local loop. It does not qualify an agent
for customer work or reproduce the separate public research studies.

## Documentation

- [Product overview](docs/product_overview.md)
- [Public research and evidence](docs/public_evidence.md)
- [Detailed quickstart](docs/quickstart.md)
- [Billing-replay sample](docs/flagship_pipeline_replay_public.md)
- [Security and local execution](docs/security_model.md)
- [Public and private material](docs/private_corpus_note.md)
- [Foundry background](docs/alpha_core_summary.md)

For a scoped product conversation, contact [amogh@veyl.work](mailto:amogh@veyl.work).
