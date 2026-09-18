# GitHub Actions integration

Use Resume the Scene as a structural gate: a pull request should not merge if the selected project-memory set is malformed or points outside the repository.

Minimal workflow:

```yaml
name: resume-scene

on:
  pull_request:
  push:

jobs:
  validate-project-memory:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.13"
      - run: python -m pip install -e .
      - run: resume-scene validate .
      - run: resume-scene checkpoint .
      - run: resume-scene resume .
```

`validate` is the gate. `checkpoint` and `resume` are useful in CI when you also want a visible, deterministic handoff packet in the run log.

For a repository that has not been bootstrapped yet, run `resume-scene init .` once in a working copy, review the generated files, and commit them. Do not run `init` on every CI run.
