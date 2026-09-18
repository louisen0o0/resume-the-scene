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


def _resolve_inside(root: Path, raw_path: object) -> Path:
    if not isinstance(raw_path, str) or "\x00" in raw_path:
        raise RSMError("E_DOC_PATH")
    relative = Path(raw_path)
    if relative.is_absolute():
        raise RSMError("E_DOC_PATH")
    root_resolved = root.resolve()
    candidate = (root_resolved / relative).resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise RSMError("E_DOC_PATH") from exc
    return candidate


def _require_file(root: Path, raw_path: object) -> Path:
    path = _resolve_inside(root, raw_path)
    if not path.is_file():
        raise RSMError("E_DOC_MISSING")
    return path


def _primary_doc(docs, doc_type: str):
    matches = [
        doc
        for doc in docs
        if doc.get("type") == doc_type and doc.get("authority") == "primary"
    ]
    if len(matches) != 1:
        raise RSMError("E_AUTHORITY")
    return matches[0]


def _optional_primary_doc(docs, doc_type: str):
    matches = [
        doc
        for doc in docs
        if doc.get("type") == doc_type and doc.get("authority") == "primary"
    ]
    if len(matches) > 1:
        raise RSMError("E_AUTHORITY")
    return matches[0] if matches else None


def load_project(root: Path):
    memory_frames = parse_file(_require_file(root, ".resume/memory.rsm"))
    memory = _one(memory_frames, "memory")
    docs = [f for k, f in memory_frames if k == "doc"]

    memory_docs = memory["docs"]
    if not isinstance(memory_docs, list) or not all(isinstance(x, str) for x in memory_docs):
        raise RSMError("E_MEMORY_SET")
    if len(memory_docs) != len(set(memory_docs)):
        raise RSMError("E_MEMORY_DUP")

    doc_ids = [d["id"] for d in docs]
    if not all(isinstance(x, str) for x in doc_ids):
        raise RSMError("E_MEMORY_SET")
    if len(doc_ids) != len(set(doc_ids)):
        raise RSMError("E_DOC_DUP")
    if set(memory_docs) != set(doc_ids):
        raise RSMError("E_MEMORY_SET")

    for doc in docs:
        _require_file(root, doc["path"])

    project_doc = _primary_doc(docs, "project")
    state_doc = _primary_doc(docs, "state")
    task_doc = _optional_primary_doc(docs, "task")

    project = _one(parse_file(_require_file(root, project_doc["path"])), "project")
    state_frames = parse_file(_require_file(root, state_doc["path"]))
    _one(state_frames, "state")
    if task_doc is None:
        task = _one(state_frames, "task")
    else:
        task = _one(parse_file(_require_file(root, task_doc["path"])), "task")

    if project["memory"] != memory["id"]:
        raise RSMError("E_MEMORY_SET")

    return project, task, memory, docs



def init_project(root: Path) -> int:
    root = root.resolve()
    if root.exists() and not root.is_dir():
        raise RSMError("E_INIT_ROOT")

    files = {
        root / "PROJECT.rsm": (
            "@project{id:#project|v:0.1|state:active|memory:#m0}\n"
            "@goal{id:#g0|state:active|accept:#a0}\n"
            "@action{id:#a0|task:#t0|op:continue|target:#project|gate:none}\n"
        ),
        root / "CURRENT.rsm": (
            "@task{id:#t0|goal:#g0|state:active|requires:[#project,#current,#protocol]|done:[]|next:#a0}\n"
            "@state{id:#s0|task:#t0|truth:[#project,#current,#protocol]|block:[]|next:#a0}\n"
        ),
        root / ".resume" / "memory.rsm": (
            "@memory{id:#m0|mode:selected|docs:[#project,#current,#protocol]}\n"
            "@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}\n"
            "@doc{id:#current|type:state|path:CURRENT.rsm|state:active|authority:primary}\n"
            "@doc{id:#protocol|type:rule|path:protocol/core.rsm|state:active|authority:primary}\n"
        ),
        root / "protocol" / "core.rsm": (
            "@schema{id:#rsm_core|v:0.1|frames:[project,memory,doc,goal,task,state,decision,evidence,action,checkpoint,msg]}\n"
            "@rule{id:#r1|op:select_memory|in:[doc]|out:memory}\n"
            "@rule{id:#r2|op:annotate_doc|in:[id,type,path,state]|out:doc}\n"
            "@rule{id:#r3|op:advance_task|in:[goal,state,evidence,decision]|out:[task,action]}\n"
            "@rule{id:#r4|op:checkpoint|in:[memory,task,hash]|out:checkpoint}\n"
            "@rule{id:#r5|op:resume|in:[checkpoint,task,memory]|out:msg}\n"
            "@rule{id:#r6|op:content_by_ref|in:[ref]|out:content}\n"
            "@rule{id:#r7|op:no_vendor_core|in:[actor]|out:opaque_actor}\n"
            "@rule{id:#r8|op:no_chat_authority|in:[conversation]|out:reference_only}\n"
            "@rule{id:#r9|op:no_history_replay|in:[checkpoint]|out:delta_or_selected}\n"
        ),
    }

    for path in files:
        if path.exists() or path.is_symlink():
            raise RSMError("E_INIT_EXISTS")

    for directory in (root / ".resume", root / "protocol"):
        if directory.exists() and not directory.is_dir():
            raise RSMError("E_INIT_LAYOUT")

    root.mkdir(parents=True, exist_ok=True)
    (root / ".resume").mkdir(parents=True, exist_ok=True)
    (root / "protocol").mkdir(parents=True, exist_ok=True)
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")

    validate_tree(root)
    return len(files)

def selected_docs(root: Path) -> list[str]:
    _, _, memory, docs = load_project(root)
    by_id = {str(doc["id"]): doc for doc in docs}
    return [encode_frame("doc", by_id[str(doc_id)]) for doc_id in memory["docs"]]


def checkpoint(root: Path) -> str:
    project, task, memory, docs = load_project(root)
    digest = hashlib.sha256()
    for doc in sorted(docs, key=lambda x: str(x["id"])):
        path = _require_file(root, doc["path"])
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


def handoff(root: Path) -> list[str]:
    validate_tree(root)
    return [*selected_docs(root), checkpoint(root), resume(root)]


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
    root_resolved = root.resolve()
    count = 0
    for path in sorted(root.rglob("*.rsm")):
        resolved = path.resolve()
        try:
            resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise RSMError("E_DOC_PATH") from exc
        parse_file(resolved)
        count += 1

    core_paths = (
        root / "PROJECT.rsm",
        root / "CURRENT.rsm",
        root / ".resume" / "memory.rsm",
    )
    if any(path.exists() or path.is_symlink() for path in core_paths):
        load_project(root)
    return count
