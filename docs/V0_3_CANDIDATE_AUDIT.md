# v0.3 candidate audit

Status: local working-branch audit only. Not a public release receipt.

## Candidate

Branch: `v0.3-expansion`

Main local expansion commits:

- `47a3421` — bootstrap + fixtures + adoption surfaces
- `d83a565` — deterministic handoff stream
- `c13cd42` — dogfood evidence update
- `bd7dcca` — adoption docs, dev package version, selected-memory cleanup

## Verification

### Unit / CLI tests

`python -m unittest discover -s tests -q`

Result:

- 27 tests
- PASS

Coverage includes:

- empty-repository init;
- existing-repository init without touching unrelated files;
- fail-closed target collision;
- fail-closed parent-layout collision;
- selected-doc order;
- exact checkpoint/resume fixtures;
- exact combined handoff fixtures;
- CLI help;
- CLI init;
- CLI machine-readable init failure;
- CLI handoff golden output.

### Root validation

`resume-scene validate .`

Result: PASS.

### Fixture validation

Validated:

- `examples/native`
- `examples/mapped`
- `examples/bootstrap`
- `examples/handoff`
- `examples/decision-handoff`
- `examples/interrupted`

All passed. Fixtures with `expected/handoff.rsm` matched the exact emitted handoff stream.

### Clean install smoke

A clean virtual environment successfully built and installed the package as:

`resume-the-scene 0.3.0.dev0`

Then the installed CLI successfully ran:

- `resume-scene init <fresh repo>`
- `resume-scene handoff <fresh repo>`

### Thin-core check

`protocol/core.rsm` has no diff from the public v0.2 baseline.

v0.3 adds usability surfaces around the protocol:

- `init`
- selected `docs` mappings
- one-command `handoff`
- additional deterministic fixtures
- CI / pre-commit / worker adoption docs

It does not add a new core frame type.

## Concrete defects found during expansion

### 1. Auxiliary status file used the .rsm extension

A local feedback-watch status file used `.rsm` even though it contained non-core frame kinds. Because tree validation intentionally parses every RSM file under the project root, this made root validation fail.

Fix: keep auxiliary operational status outside the `.rsm` extension.

### 2. Init parent-directory collision could mutate before failing

If `protocol` or `.resume` existed as a regular file, the first init implementation could create another directory before hitting the parent collision.

Fix: preflight parent layout collisions before any init mutation.

### 3. Dogfood memory loaded example documents

The repository's own selected memory included example task/evidence/decision documents, which caused normal root resume packets to ask workers to load example material.

Fix: examples remain fixtures on disk but are no longer part of the repository's active selected memory.

## Release boundary

Still not done:

- no public v0.3 branch/PR push;
- no v0.3 tag;
- no package-registry publication;
- no claim of external adoption or production effectiveness.

Those remain external publication gates.
