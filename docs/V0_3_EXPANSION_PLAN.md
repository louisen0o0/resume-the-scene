# v0.3 Expansion Plan

Status: COMPLETE / RELEASED
Release: `v0.3.0`
Release URL: https://github.com/louisen0o0/resume-the-scene/releases/tag/v0.3.0

The project is still new, so lack of public feedback is not treated as a blocking signal. Feedback collection is passive. v0.3 widened the usable surface without making the core protocol heavier.

## Completed scope

### 1. First use without hand-authoring RSM files

DONE.

`resume-scene init <repo>` creates the minimal Project / Current / Memory / Protocol surface, validates immediately, and refuses to overwrite existing target files.

### 2. Real handoff fixtures

DONE.

Deterministic fixtures now cover:
- fresh repository bootstrap;
- existing repository mapped in place;
- verified work that must be skipped;
- an active decision that survives worker change;
- an interrupted task with a precise next action.

### 3. Adoption surfaces without new protocol layers

DONE.

Included:
- GitHub Actions validation;
- pre-commit validation;
- generic worker handoff notes;
- vendor-neutral worker prompt;
- state-editing guidance;
- existing-repository adoption guidance.

### 4. Cold-start usability

DONE.

A repository-root `./resume-scene` wrapper allows a fresh worker to validate and hand off from a clone without an editable install.

Cold-start Canary 2 recovered the active task, completed work, trusted evidence, active decision, and exact next action from the repository itself without relying on chat history.

### 5. Release verification

DONE.

- PR #4 merged to `main`;
- GitHub CI passed on Python 3.11, 3.12, and 3.13;
- package metadata finalized to `0.3.0`;
- tag and GitHub Release `v0.3.0` published;
- a fresh public clone from tag `v0.3.0` passed `./resume-scene validate .` and `./resume-scene handoff .`.

## Explicit non-goals retained

- no vector database;
- no chat archive;
- no autonomous background memory daemon;
- no model-vendor identity in the core protocol;
- no speculative schema expansion without a concrete handoff case.

## Current next action

None. v0.3 is complete. Keep feedback passive; start a new task only when a concrete new requirement or real-world failure justifies it.
