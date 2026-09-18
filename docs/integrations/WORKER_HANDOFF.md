# Worker handoff integration

Resume the Scene does not need a worker-specific protocol adapter for the basic handoff.

A worker only needs two capabilities:

1. read the files referenced by the selected memory set;
2. run `resume-scene handoff <project>` or consume the equivalent `@doc` + checkpoint + resume frames.

A generic handoff loop is:

```text
1. run: resume-scene handoff .
2. resolve the IDs in load:[...] against the emitted @doc ID-to-path mappings
3. load only those selected files
4. do not redo IDs listed in skip:[...]
5. continue from next:#...
6. update the project-owned state files when verified state changes
7. run: resume-scene checkpoint .
```

Example mapping + packet:

```text
@doc{id:#e2|type:evidence|path:memory/evidence/E001.rsm|state:active|authority:primary}
@doc{id:#d2|type:decision|path:memory/decisions/D001.rsm|state:active|authority:primary}
@msg{op:resume|task:#t2|load:[#p2,#c2,#t2,#e2,#d2]|skip:[#e2]|next:#a2}
```

Interpretation:

- `load` is the selected working set, not a request to replay the full project history;
- `skip` is verified work that should not be repeated merely because the worker changed;
- `next` is the exact continuation point.

The core format deliberately does not encode worker or model identity. Tool-specific instructions belong in integration documentation or project-local rules, not in the core protocol.
