# 恢复现场吧 / Resume the Scene

**面向 AI 协作的项目记忆：从已验证的任务状态继续，而不是重读聊天记录。**  
**Project memory for AI work: resume from verified task state, not chat history.**

[![CI](https://github.com/louisen0o0/resume-the-scene/actions/workflows/ci.yml/badge.svg)](https://github.com/louisen0o0/resume-the-scene/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 中文

对话记忆保存“说过什么”，知识库 / RAG 帮你找到“资料里有什么”。但项目真正中断时，丢失的往往是另一件事：

> **现在什么是真的，为什么相信它，哪些已经做完不该重做，下一步从哪里继续。**

**恢复现场吧**把这类信息定义为 **Project Memory（项目记忆）**，并让它跟项目本身一起存在，而不是依赖某一次会话。

它不要求特定模型，不要求向量数据库，也不要求保存完整聊天历史。它只给 AI 一个稳定、可校验的接手面：当前有效的项目记忆、任务状态、证据引用和 checkpoint。

### 四个变化

**记忆作用域 · Memory Scope（新记忆体）**  
只声明哪些项目文件构成当前有效记忆；不复制整仓库，也不把历史全部塞回上下文。

**项目结构 · Project Layout（新结构）**  
新项目可以直接采用标准布局；旧项目也可以原地映射，不需要为了接入而迁库。

**语义标注 · Semantic Typing（新标注）**  
让 Goal、State、Task、Decision、Evidence、Artifact 等角色显式可判，不再让 AI 靠文件名和自然语言猜文档用途。

**续接语言 · Resumption Protocol（新语言）**  
AI 不再交换一大段“背景说明”，而是交换 typed、可解析、可验证的任务状态与引用。

```text
@task{id:#t42|goal:#g1|state:active|done:[#e69]|next:#a7}
@msg{op:resume|task:#t42|load:[#current,#e81]|skip:[#e69]|next:#a7}
```

一次会话可以结束，机器可以重启，执行者可以更换；项目仍然保留同一个 TASK 的真实落点。

### 保持很薄

- 项目文件继续是真实事实源；
- 不保存完整聊天记录；
- 不要求把 Prompt / Response 纳入统一记忆；
- 不要求向量数据库；
- 核心协议不绑定模型品牌；
- 恢复工作时不需要全量重放历史。

### 最小模型

```text
PROJECT
  -> MEMORY
  -> DOCUMENT
  -> TASK
  -> EVIDENCE / DECISION
  -> CHECKPOINT
  -> RESUME
```

Project Memory 保存的是选择、类型、引用、状态与校验信息，不替代项目正文。

### 为什么叫“恢复现场吧”

真正需要恢复的通常不是窗口，而是**工作的落点**。

当前 Task、有效决定、已通过证据、阻塞、下一动作，以及这些事实分别来自哪里——这些还在，项目现场就还在。

---

## English

Conversation memory preserves **what was said**. Knowledge memory / RAG retrieves **what information is available**. But when project work is interrupted, a different kind of continuity is usually missing:

> **What is true now, why it is trusted, what has already been completed, and what should happen next.**

**Resume the Scene** treats that continuity as **Project Memory** and keeps it with the project itself instead of tying it to a single conversation.

It does not require a particular model, a vector database, or a full chat archive. It gives AI workers a stable, machine-verifiable handoff surface: the active memory set, typed task state, evidence references, and a checkpoint.

### Four changes

**Memory Scope**  
Declare which project files form the active memory set. Do not copy the whole repository or replay all history into context.

**Project Layout**  
Use a native layout for new projects, or map an existing repository in place without migrating it.

**Semantic Typing**  
Make Goal, State, Task, Decision, Evidence, and Artifact explicit so document roles do not have to be inferred from filenames or prose.

**Resumption Protocol**  
Exchange typed, parseable, verifiable task state and references instead of repeating long natural-language handoff notes.

```text
@task{id:#t42|goal:#g1|state:active|done:[#e69]|next:#a7}
@msg{op:resume|task:#t42|load:[#current,#e81]|skip:[#e69]|next:#a7}
```

A session can end. A machine can restart. A worker can change. The project can still preserve the same verified TASK handoff point.

### Thin by design

- project files remain the source of truth;
- no full conversation archive;
- no requirement to store prompts or responses;
- no vector database requirement;
- no model-vendor identity in the core protocol;
- no full-history replay just to resume work.

### Minimal model

```text
PROJECT
  -> MEMORY
  -> DOCUMENT
  -> TASK
  -> EVIDENCE / DECISION
  -> CHECKPOINT
  -> RESUME
```

Project Memory stores selection, type, references, state, and verification metadata. It does not replace the project itself.

### Why “Resume the Scene”?

What usually gets lost is not the file. It is the **working point**.

If the current Task, accepted decisions, verified evidence, blockers, next action, and their sources survive, the project can resume from the same scene.

---

## Quick start / 快速开始

From a cloned repository, no editable install is required for the read-only handoff path:

从源码仓库直接接手时，不需要先做 editable install：

```bash
./resume-scene validate .
./resume-scene handoff .
```

Installed package path / 安装后也可以：

```bash
python -m pip install -e .
resume-scene validate .
resume-scene handoff .
```

### v0.3 working branch: bootstrap a fresh repository / 初始化一个新仓库

The `v0.3-expansion` branch adds a fail-closed `init` path so a new repository does not need hand-authored RSM files before the first validation. It refuses to overwrite any existing target file.

`v0.3-expansion` 工作分支新增了 fail-closed 的 `init`：新仓库第一次接入时不用手写 RSM 文件；如果目标文件已经存在，它会拒绝覆盖。

```bash
./resume-scene init /path/to/project
./resume-scene validate /path/to/project
./resume-scene handoff /path/to/project
```

If the package is already installed, the same commands work without the leading `./`.

Expected machine output / 预期机器输出：

```text
@doc{id:#project|type:project|path:PROJECT.rsm|state:active|authority:primary}
...
@checkpoint{id:#c_...|project:#resume_scene|task:#t0|memory:#m0|fingerprint:sha256:...}
@msg{op:resume|task:#t0|load:[#project,#current,#protocol,...]|skip:[]|next:#a0}
```

`handoff` is only a convenience stream: selected `@doc` mappings + the existing deterministic checkpoint + resume packet. It adds no new core frame type.

`handoff` 只是便利输出：选中的 `@doc` 映射 + 现有 checkpoint + resume；不会增加新的核心 frame 类型。

### 30-second handoff demo / 30 秒接手示例

Run the handoff fixture as if a different AI worker is arriving after verified work has already been completed:

把 `examples/handoff` 当成“上一位 AI 已完成部分工作、下一位 AI 现在接手”的现场：

```bash
resume-scene validate examples/handoff
resume-scene checkpoint examples/handoff
resume-scene resume examples/handoff
```

The resume packet is deterministic:

```text
@msg{op:resume|task:#t2|load:[#p2,#c2,#t2,#e2,#d2]|skip:[#e2]|next:#a2}
```

`skip:[#e2]` tells the next worker not to redo verified evidence. `next:#a2` gives the exact continuation point. No chat transcript is required.

`skip:[#e2]` 表示已验证工作不要重做，`next:#a2` 指向明确的下一动作；整个接手过程不依赖上一段聊天记录。

The repository dogfoods its own format: its current project state is represented by `PROJECT.rsm`, `CURRENT.rsm`, and `.resume/memory.rsm`.

仓库本身也使用同一套格式记录自己的项目现场：`PROJECT.rsm`、`CURRENT.rsm` 与 `.resume/memory.rsm`。

License / 许可证：MIT.

## v0.2

`v0.2` keeps the core thin while making it safer and easier to adopt in real repositories:

- existing repositories can map project, state, task, evidence, and decision files in place through `.resume/memory.rsm`;
- worker-neutral handoff fixtures pin exact checkpoint and resume outputs;
- document paths, symlink escapes, duplicate document IDs, and duplicate memory entries now fail closed.

`v0.2` 保持薄核心，同时补上真实仓库接入与安全边界：

- 旧项目可通过 `.resume/memory.rsm` 原地映射 Project / State / Task / Evidence / Decision，无需迁目录；
- 跨 AI 接手示例固定了 checkpoint 与 resume 的精确机器输出；
- 路径越界、符号链接逃逸、重复文档 ID 与重复记忆项均按 fail-closed 处理。

Mapped-layout example / 原地映射示例：`examples/mapped`.

Additional handoff fixtures / 更多接手示例：

- `examples/decision-handoff` — an active decision survives a worker change;
- `examples/interrupted` — verified work is skipped and one precise next action survives an interruption.

Integration and adoption notes / 接入与采用说明：

- editing the five pieces of current state: `docs/EDITING_STATE.md`
- adopting an existing repository: `docs/MIGRATING_EXISTING_REPO.md`
- GitHub Actions: `docs/integrations/GITHUB_ACTIONS.md`
- pre-commit: `docs/integrations/PRE_COMMIT.md`
- generic worker handoff: `docs/integrations/WORKER_HANDOFF.md`
- copyable vendor-neutral worker prompt: `docs/integrations/WORKER_PROMPT.md`