# Veyl product overview

Updated September 9, 2026.

Veyl began with software-engineering evaluation environments. The product now
addresses the operating question around an enterprise agent: what work can this
specific deployment own, what needs human review, and when must it stop?

## The reliability lifecycle

1. Define the workflow, expected outcome, authority, and important failure cases.
2. Build scenarios from approved operating history and validate the checks.
3. Evaluate a versioned deployment against those scenarios.
4. Test changes to the deployment and establish its permitted scope.
5. Track outcomes and refresh affected evidence when dependencies change.

The result belongs to the tested workflow and setup. It is not a general model
ranking. See the [published methodology](https://veyl.work/methodology).

## Product areas

**Coding agents.** Engineering history supplies concrete cases where apparently
successful changes can violate business rules. Veyl evaluates the complete agent
setup and the review boundary around it. This is the domain of the current public
studies. [Coding-agent evaluation](https://veyl.work/coding-agent-evaluation)

**Veyl Private.** Deployment planning combines approved models, organizational
knowledge, agent tools, permissions, and evaluation. The infrastructure may be
customer-controlled or a separately scoped local system. Architecture, capacity,
provider exposure, and support are defined for each engagement.
[Private AI](https://veyl.work/private-ai)

**Veyl Physical.** The physical-systems direction begins with drone inspection:
define the mission and operating envelope, qualify the system, review findings,
and connect them to an operational report. The mission, human authority, and
revalidation conditions are part of the scope.
[Physical AI](https://veyl.work/physical)

## Where this repository fits

Foundry Lite provides an inspectable local example of task execution and visible
behavior checks. It is intentionally small. It does not implement the managed
product's deployment controls or its private evaluation system, and does not
provide private model hosting, hardware, or flight-control software.

Use the [quickstart](quickstart.md) to try the code and the
[evidence guide](public_evidence.md) to inspect the separate research. Product
availability and the permitted data boundary are agreed through a scoped
conversation with [Veyl](mailto:amogh@veyl.work).
