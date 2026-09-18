from __future__ import annotations

import sys
from pathlib import Path

from .core import RSMError, checkpoint, encode_frame, init_project, resume, validate_tree


def main() -> int:
    try:
        if len(sys.argv) < 2:
            print("@result{op:cli|state:error|code:E_ARG}")
            return 2
        op = sys.argv[1]
        if op in {"help", "--help", "-h"}:
            print(
                "usage: resume-scene <init|validate|checkpoint|resume> [project]\n"
                "\n"
                "init        create the minimal project-memory files without overwriting targets\n"
                "validate    validate RSM files and selected project memory\n"
                "checkpoint  emit a deterministic checkpoint fingerprint\n"
                "resume      emit the selected load / skip / next handoff packet"
            )
            return 0
        root = Path(sys.argv[2] if len(sys.argv) > 2 else ".").resolve()
        if op == "init":
            count = init_project(root)
            print(encode_frame("result", {"op": "init", "state": "pass", "count": str(count)}))
            return 0
        if op == "validate":
            count = validate_tree(root)
            print(encode_frame("result", {"op": "validate", "state": "pass", "count": str(count)}))
            return 0
        if op == "checkpoint":
            print(checkpoint(root))
            return 0
        if op == "resume":
            print(resume(root))
            return 0
        print("@result{op:cli|state:error|code:E_OP}")
        return 2
    except (RSMError, OSError) as exc:
        code = exc.code if isinstance(exc, RSMError) else "E_IO"
        print(f"@result{{op:cli|state:error|code:{code}}}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
