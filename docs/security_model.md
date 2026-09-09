# Security and execution boundaries

## Foundry Lite runs on your machine

Lite copies the example workspace, runs its configured checks as local shell
commands, and saves an event log. An optional `--command` also runs locally.
These processes inherit your user's permissions and environment. The copied
workspace is not an isolation boundary.

Use trusted task definitions and code. The included Dockerfile describes the
example environment; the Lite runner does not start Docker or enforce a
container boundary. It does not restrict filesystem access or network access.

The selected `--output` directory is replaced on each run. Use a dedicated
directory such as `out/starter`, never a directory containing work you need to
keep. Local logs can contain command output and paths; inspect them before sharing.

## Public release scope

The runnable package originates from an explicit allowlist: the public README,
package metadata, public docs, Lite runner, and public example. Documentation is
maintained against the released code and published Veyl product pages.
`PUBLIC_EXPORT_MANIFEST.json` records the original code export and subsequent
documentation updates.

Private implementation, grading material, internal experiments, customer
information, and operational configuration are excluded. See the
[public/private boundary](private_corpus_note.md).

## Managed product boundaries

The managed product has a separate, engagement-specific execution and data
boundary. Its controls are not provided by installing Foundry Lite. The public
[security page](https://veyl.work/security) describes infrastructure options,
provider disclosure, access, retention, and the current certification posture.

For a security concern involving this repository, contact
[amogh@veyl.work](mailto:amogh@veyl.work) without including sensitive data in a
public issue.
