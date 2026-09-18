# v0.3 release notes — draft

Not published. Working branch only. Package metadata is `0.3.0.dev0` until the external release gate is opened.

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

The repository now includes working notes for:

- GitHub Actions validation;
- pre-commit validation;
- generic worker handoff integration without adding vendor identity to the core protocol.

### Packaging smoke-tested

A clean virtual environment can build/install the package and run:

```text
resume-scene --help
resume-scene init <repo>
resume-scene validate <repo>
resume-scene resume <repo>
```

## What does not change

The core is still deliberately small:

- no chat archive;
- no vector database requirement;
- no background memory daemon;
- no model-vendor identity in core state;
- no speculative schema layer added for this release.

## Release gates still open

Before any public v0.3 tag/package release:

1. final branch audit;
2. CI pass on the public branch/PR;
3. version bump and changelog finalization;
4. explicit external publish decision.
