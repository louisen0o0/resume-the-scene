# pre-commit integration

The useful local gate is simple: reject a commit if the current selected memory set is structurally invalid.

Until a release containing the hook metadata is published, a repository can use a local hook:

```yaml
repos:
  - repo: local
    hooks:
      - id: resume-scene-validate
        name: validate Resume the Scene project memory
        entry: resume-scene validate .
        language: system
        pass_filenames: false
```

Install the package in the environment used by pre-commit first:

```bash
python -m pip install -e /path/to/resume-the-scene
pre-commit install
```

The hook should validate only. It should not mutate project memory automatically during a commit.
