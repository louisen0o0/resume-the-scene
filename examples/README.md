# Examples

Each fixture is a small, worker-neutral handoff case with deterministic checkpoint/resume output.

- `native` — standard in-repository layout.
- `mapped` — an existing repository maps project/state/evidence/decision files in place.
- `bootstrap` — the minimal repository created by `resume-scene init`.
- `handoff` — verified work survives a worker/session/machine change.
- `decision-handoff` — verified evidence and an active decision both survive the handoff.
- `interrupted` — an interrupted task keeps verified work in `skip` and preserves one exact next action.

The examples are intentionally small. They are compatibility fixtures, not templates for a larger framework.
