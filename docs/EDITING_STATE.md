# Editing project state

Resume the Scene keeps the core small, so v0.3 still treats project state as project-owned text files rather than hiding mutations behind a large state service.

The five things worth keeping explicit are:

1. **Current Task** — what is active now;
2. **Done / Skip** — verified work that should not be repeated;
3. **Trusted Evidence** — facts the next worker may rely on;
4. **Active Decision** — choices that still constrain the work;
5. **Next Action** — the exact continuation point.

## Current Task and Next Action

`CURRENT.rsm` carries the active task and state:

```text
@task{id:#t0|goal:#g0|state:active|requires:[#e1,#d1]|done:[#e1]|next:#a1}
@state{id:#s0|task:#t0|truth:[#e1,#d1]|block:[]|next:#a1}
```

`PROJECT.rsm` defines the action referred to by `next`:

```text
@action{id:#a1|task:#t0|op:continue|target:#artifact1|gate:none}
```

The important invariant is not the wording of `op`. It is that `task.next`, `state.next`, and the active action ID agree.

## Done / Skip

`task.done` is the set emitted as `skip:[...]` in the resume packet.

Only place IDs there after the work is actually verified. A new worker should be able to trust that `skip` means “do not redo this just because the worker changed.”

## Trusted Evidence

Evidence lives in a normal RSM file:

```text
@evidence{id:#e1|task:#t0|subject:#artifact1|state:valid|ref:memory/evidence/E001.rsm|hash:none}
```

Then map the evidence into the selected memory set:

```text
@doc{id:#e1|type:evidence|path:memory/evidence/E001.rsm|state:active|authority:primary}
```

If the task depends on it, include `#e1` in `requires` / `truth`. If it is completed work that should not be repeated, also include it in `done`.

## Active Decision

A decision uses the existing decision frame:

```text
@decision{id:#d1|task:#t0|state:active|supersedes:none|next:#a1}
```

Map it into memory with a `type:decision` document. The purpose is not to preserve every discussion. Preserve the decision that still governs the current work.

## Safe editing loop

After changing project state:

```bash
resume-scene validate .
resume-scene checkpoint .
resume-scene handoff .
```

The handoff stream should now show the intended document mappings, `skip` set, and exact `next` action.

Do not add a fact to `done`, `truth`, or active decisions merely because an AI proposed it. Promote it only after the project has evidence or an explicit decision that makes it authoritative.
