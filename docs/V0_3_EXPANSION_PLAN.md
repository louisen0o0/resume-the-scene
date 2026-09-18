# v0.3 Expansion Plan

Status: active working plan — implementation pass 2 complete
Branch: `v0.3-expansion`

The project is still new, so lack of public feedback is not treated as a blocking signal. Feedback collection stays passive while v0.3 focuses on widening the usable surface without making the core protocol heavy.

## Priority order

### 1. Make first use possible without hand-authoring RSM files — DONE

Add a fail-closed `resume-scene init <repo>` path for a new repository.

Acceptance:
- creates only the minimal Project / Current / Memory / Protocol files;
- refuses to overwrite any existing target file;
- the generated repository immediately passes `validate`;
- `checkpoint` is deterministic;
- `resume` returns a valid `load / skip / next` packet.

Why first:
Current quick start assumes the memory files already exist. That is acceptable for the author, but it is avoidable setup friction for a new user.

### 2. Add more real handoff fixtures — DONE FOR PASS 1

Expand examples around distinct continuation problems rather than more protocol concepts:
- fresh repository bootstrap;
- existing repository mapped in place;
- verified work that must be skipped;
- active decision that must survive worker change;
- interrupted task with a precise next action.

Acceptance:
Every fixture pins exact checkpoint/resume output and remains worker-neutral.

### 3. Add adoption surfaces, not new protocol layers — DONE FOR PASS 1

Prepare:
- GitHub Actions validation example;
- pre-commit example;
- concise worker integration notes for common AI coding tools while keeping the core vendor-neutral.

These belong in docs/adapters, not the protocol core.

### 4. Prepare install/distribution improvements — LOCAL SMOKE PASS

Prepare packaging and release artifacts so a stranger does not need an editable clone forever.

External publication (for example a package registry release) remains a separate publish gate.

## Explicit non-goals for this expansion

- no vector database;
- no chat archive;
- no autonomous background memory daemon;
- no model-vendor identity in the core protocol;
- no speculative schema expansion without a concrete handoff case;
- no waiting for public feedback before continuing basic usability work.

## Current next action

Keep expanding only along verified usability seams. Pass 2 added a deterministic `handoff` stream, CLI tests, state-editing/adoption docs, and clean-install packaging smoke. Next: run a final thin-core audit and stop adding protocol concepts unless a concrete cold-start failure demands them. External publication remains gated.