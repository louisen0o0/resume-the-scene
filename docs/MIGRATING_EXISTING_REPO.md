# Adopting Resume the Scene in an existing repository

There are two adoption paths.

## Path A — bootstrap the minimal standard layout

If the repository does not already have project-memory files:

```bash
resume-scene init .
resume-scene validate .
resume-scene handoff .
```

`init` does not delete or rewrite unrelated repository files. It refuses to run if one of its own target files already exists.

After bootstrap, edit `PROJECT.rsm` and `CURRENT.rsm` to describe the real task instead of the starter placeholders.

## Path B — map existing state files in place

If the repository already has its own project/state/evidence/decision files and moving them would be disruptive, keep them where they are and map them from `.resume/memory.rsm`.

See `examples/mapped` for a deterministic fixture where project, state, task, evidence, and decision files stay in legacy paths.

The mapping layer should identify the current authoritative files. It should not copy the entire repository into memory.

## Choosing between them

Use the smallest path that makes the current working point explicit:

- new or simple repo → bootstrap;
- established repo with existing state files → mapped layout.

Do not reorganize a repository merely to satisfy the tool.
