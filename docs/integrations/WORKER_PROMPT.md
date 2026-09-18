# Generic worker prompt

This is a vendor-neutral handoff instruction for a worker that can run shell commands and read files.

```text
You are continuing an existing project. Do not reconstruct project state from chat history first.

1. Run: resume-scene handoff .
2. Read the emitted @doc mappings.
3. Load only the IDs listed in the final @msg load:[...].
4. Treat skip:[...] as verified work that must not be repeated without new contradictory evidence.
5. Continue from next:#...
6. Project files remain the source of truth. Chat history is reference-only unless the project explicitly promotes a fact into project state.
7. When verified state changes, update the project-owned RSM files, run resume-scene validate ., and emit a new checkpoint/handoff.
8. Do not add model/vendor identity to the core protocol unless the project explicitly requires it outside the core state.
```

This prompt does not grant the worker authority to overwrite project decisions. It tells the worker where the current authority lives and how to resume from it.
