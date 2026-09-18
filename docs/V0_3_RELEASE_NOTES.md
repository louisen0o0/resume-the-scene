# v0.3.0 release notes

Released after the v0.3 expansion branch passed local validation, GitHub CI on Python 3.11/3.12/3.13, and a second cold-start handoff canary with a fresh worker.

## What changes

### Bootstrap without hand-writing RSM files

`resume-scene init <repo>` creates the minimal Project / Current / Memory / Protocol surface and immediately validates it.

It is fail-closed on existing target files: if one of the files it owns already exists, it refuses to overwrite anything.

### One-command handoff stream

`resume-scene handoff <repo>` emits the selected `@doc` ID-to-path mappings, deterministic checkpoint, and resume packet in one machine-readable stream. It reuses existing core frame types.

### More continuation fixtures

New deterministic fixtures cover:

- fresh repository bootstrap;
- an active decision that survives worker change;
- an interrupted task with verified work that should not be repeated.

### Adoption surfaces

The repository includes working notes for:

- GitHub Actions validation;
- pre-commit validation;
- generic worker handoff integration without adding vendor identity to the core protocol;
- editing the five pieces of current project state;
- adopting an existing repository in place.

### Cold-start usability

A repository-root `./resume-scene` wrapper allows a fresh worker to validate and hand off from a clone without an editable install.

A second fresh-worker canary successfully recovered the active task, completed work, trusted evidence, active decision, and exact next action from the project itself without relying on chat history.

### Packaging smoke-tested

A clean virtual environment can build/install the package and run:

```text
resume-scene --help
resume-scene init <repo>
resume-scene validate <repo>
resume-scene handoff <repo>
```

## What does not change

The core is still deliberately small:

- no chat archive;
- no vector database requirement;
- no background memory daemon;
- no model-vendor identity in core state;
- no speculative schema layer added for this release.

`protocol/core.rsm` remains unchanged from v0.2.
