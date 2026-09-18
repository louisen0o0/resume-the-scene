# Worker handoff integration

Resume the Scene does not need a worker-specific protocol adapter for the basic handoff.

A worker only needs two capabilities:

1. read the files referenced by the selected memory set;
2. run `resume-scene resume <project>` or consume the equivalent deterministic packet.

A generic handoff loop is:

```text
1. run: resume-scene validate .
2. run: resume-scene resume .
3. load only the IDs listed in load:[...]
4. do not redo IDs listed in skip:[...]
5. continue from next:#...
6. update the project-owned state files when verified state changes
7. run: resume-scene checkpoint .
```

Example packet:

```text
@msg{op:resume|task:#t2|load:[#p2,#c2,#t2,#e2,#d2]|skip:[#e2]|next:#a2}
```

Interpretation:

- `load` is the selected working set, not a request to replay the full project history;
- `skip` is verified work that should not be repeated merely because the worker changed;
- `next` is the exact continuation point.

The core format deliberately does not encode worker or model identity. Tool-specific instructions belong in integration documentation or project-local rules, not in the core protocol.
