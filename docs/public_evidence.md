# Public research and evidence

Veyl publishes coding-workflow studies so readers can inspect the distinction
between a passing test suite and a correct business outcome. These are independent
studies of public repositories, not customer engagements or endorsements by the
organizations named below.

| Study | Published observation | Scope of the conclusion |
| --- | --- | --- |
| [Ramp CLI](https://veyl.work/ramp-coding-agent-study) | All 18 final repairs passed the disclosed checks; seven failed held-out business rules. | Ordinary checks were insufficient for these reconstructed workflows. |
| [Brex Substation](https://veyl.work/brex-bounded-delegation-study) | 18/18 total held-out runs passed across two deployments and three workflow families. | Those three lanes qualified for bounded delegation under the tested conditions. |
| [Moov ACH](https://veyl.work/moov-ci-gap-study) | Twenty of 32 seeded defects survived the repository's 71-package suite. | The mutation study identified gaps in coverage of payment behavior. |

The full study pages supply methods, source references, results, and limitations.
Results from different studies must not be combined into a single agent score.
The ACH experiment is a test-coverage study, not an agent success-rate trial.

These studies do not establish performance on private production systems or
validate every broader enterprise or physical workflow. See the
[research index](https://veyl.work/evidence) for the current published record.

## Try the public example

The [billing-replay sample](flagship_pipeline_replay_public.md) is a separate
teaching example with visible fixtures and an included passing implementation.
It illustrates the local mechanics; it does not rerun or reproduce the studies
above. Its checks are intentionally visible to anyone using this repository.
