from __future__ import annotations

import hashlib
import re
from pathlib import Path


class RSMError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


_FRAME = re.compile(r"^@([a-z_][a-z0-9_]*)\{(.*)\}$")
_KEY = re.compile(r"^[a-z_][a-z0-9_]*$")

_REQUIRED = {
    "project": {"id", "v", "state", "memory"},
    "memory": {"id", "mode", "docs"},
    "doc": {"id", "type", "path", "state", "authority"},
    "goal": {"id", "state", "accept"},
    "task": {"id", "goal", "state", "requires", "done", "next"},
    "state": {"id", "task", "truth", "block", "next"},
    "decision": {"id", "task", "state"},
    "evidence": {"id", "task", "subject", "state", "ref", "hash"},
    "action": {"id", "task", "op", "target", "gate"},
    "checkpoint": {"id", "project", "task", "memory", "fingerprint"},
    "msg": {"op", "task", "load", "skip", "next"},
    "schema": {"id", "v", "frames"},
    "rule": {"id", "op", "in", "out"},
    "result": {"op", "state"},
}


def _split_top(text: str, sep: str) -> list[str]:
    out: list[str] = []
    start = 0
    depth = 0
    for i, ch in enumerate(text):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth < 0:
                raise RSMError("E_BRACKET")
        elif ch == sep and depth == 0:
            out.append(text[start:i])
            start = i + 1
    if depth != 0:
        raise RSMError("E_BRACKET")
    out.append(text[start:])
    return out


def parse_value(raw: str):
    if raw.startswith("["):
        if not raw.endswith("]"):
            raise RSMError("E_LIST")
        inner = raw[1:-1]
        if inner == "":
            return []
        return [parse_value(x) for x in _split_top(inner, ",")]
    if any(ch.isspace() for ch in raw) or raw == "":
        raise RSMError("E_ATOM")
    return raw


def parse_frame(line: str) -> tuple[str, dict[str, object]]:
    line = line.strip()
    match = _FRAME.match(line)
    if not match:
        raise RSMError("E_FRAME")
    kind, body = match.groups()
    fields: dict[str, object] = {}
    if body:
        for part in _split_top(body, "|"):
            if ":" not in part:
                raise RSMError("E_FIELD")
            key, raw = part.split(":", 1)
            if not _KEY.match(key):
                raise RSMError("E_KEY")
            if key in fields:
                raise RSMError("E_DUP")
            fields[key] = parse_value(raw)
    validate_frame(kind, fields)
    return kind, fields


def validate_frame(kind: str, fields: dict[str, object]) -> None:
    required = _REQUIRED.get(kind)
    if required is None:
        raise RSMError("E_KIND")
    if not required.issubset(fields):
        raise RSMError("E_REQUIRED")


def encode_value(value) -> str:
    if isinstance(value, list):
        return "[" + ",".join(encode_value(v) for v in value) + "]"
    return str(value)


def encode_frame(kind: str, fields: dict[str, object]) -> str:
    validate_frame(kind, fields)
    body = "|".join(f"{k}:{encode_value(v)}" for k, v in fields.items())
    return f"@{kind}{{{body}}}"


def parse_file(path: Path) -> list[tuple[str, dict[str, object]]]:
    frames: list[tuple[str, dict[str, object]]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            frames.append(parse_frame(raw))
    return frames


def _one(frames, kind: str):
    matches = [f for k, f in frames if k == kind]
    if len(matches) != 1:
        raise RSMError("E_CARDINALITY")
    return matches[0]


def load_project(root: Path):
    project = _one(parse_file(root / "PROJECT.rsm"), "project")
    current_frames = parse_file(root / "CURRENT.rsm")
    task = _one(current_frames, "task")
    memory_frames = parse_file(root / ".resume" / "memory.rsm")
    memory = _one(memory_frames, "memory")
    docs = [f for k, f in memory_frames if k == "doc"]
    ids = {d["id"] for d in docs}
    if set(memory["docs"]) != ids:
        raise RSMError("E_MEMORY_SET")
    return project, task, memory, docs


def checkpoint(root: Path) -> str:
    project, task, memory, docs = load_project(root)
    digest = hashlib.sha256()
    for doc in sorted(docs, key=lambda x: str(x["id"])):
        path = root / str(doc["path"])
        if not path.is_file():
            raise RSMError("E_DOC_MISSING")
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(str(doc["id"]).encode())
        digest.update(b"\0")
        digest.update(str(doc["path"]).encode())
        digest.update(b"\0")
        digest.update(file_hash.encode())
        digest.update(b"\n")
    fp = "sha256:" + digest.hexdigest()
    cid = "#c_" + digest.hexdigest()[:12]
    return encode_frame(
        "checkpoint",
        {
            "id": cid,
            "project": project["id"],
            "task": task["id"],
            "memory": memory["id"],
            "fingerprint": fp,
        },
    )


def resume(root: Path) -> str:
    _, task, memory, _ = load_project(root)
    return encode_frame(
        "msg",
        {
            "op": "resume",
            "task": task["id"],
            "load": memory["docs"],
            "skip": task["done"],
            "next": task["next"],
        },
    )


def validate_tree(root: Path) -> int:
    count = 0
    for path in sorted(root.rglob("*.rsm")):
        parse_file(path)
        count += 1
    return count
