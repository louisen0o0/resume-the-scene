# 恢复现场吧 / Resume the Scene

**让任何 AI 从项目真正停下来的地方继续，而不是重新读一遍聊天。**  
**Let any AI continue from the real project state instead of rereading the conversation.**

---

## 中文

聊天记忆解决“我们说过什么”。知识库 / RAG 解决“资料里有什么”。

**恢复现场吧**处理第三件事：

> **这个项目现在做到哪里，为什么是这个状态，什么已经完成不能重做，下一步从哪里继续。**

它不是聊天记录，不是向量数据库，也不绑定某一家模型。

Claude、Codex、Gemini、本地模型或未来任何 Agent，都只是临时 Worker。项目记忆独立存在。

### 四个极薄的层

**新记忆体**：只声明哪些文件构成当前项目记忆，不复制整仓库。  
**新结构**：给新项目标准布局，也允许旧项目原地映射，不要求迁库。  
**新标注**：让 AI 明确知道每份文件是 Goal、State、Task、Decision、Evidence 还是 Artifact。  
**新语言**：AI 之间不再搬运长篇解释，只交换 typed、可验证、可恢复的项目状态。

```text
@task{id:#t42|goal:#g1|state:active|done:[#e69]|next:#a7}
@msg{op:resume|task:#t42|load:[#current,#e81]|skip:[#e69]|next:#a7}
```

这意味着一次 AI 会话可以结束、浏览器可以关闭、机器可以重启、Worker 可以更换；只要项目文件还在，下一位 AI 就能从同一个 TASK 继续。

### 它刻意不做什么

- 不保存完整聊天记录；
- 不要求把 Prompt / Response 放入统一记忆；
- 不要求向量数据库；
- 不把任何模型品牌写进核心协议；
- 不接管你的项目文件；
- 不为了恢复上下文而重新读取所有历史。

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

正文仍是事实来源；项目记忆只保存选择、类型、引用、状态和校验信息。

### 为什么叫“恢复现场吧”

真正丢失的通常不是文件，而是**工作的落点**。

一个项目真正需要恢复的是：当前 Task、有效决定、已通过证据、阻塞、下一动作，以及这些事实分别来自哪里。

---

## English

Conversation memory answers: **“What did we talk about?”**  
Knowledge memory / RAG answers: **“What information exists?”**

**Resume the Scene** addresses a third problem:

> **Where is this project now, why is that state trusted, what must not be repeated, and what should happen next?**

It is not a chat archive, not a vector database, and not tied to any model vendor.

Claude, Codex, Gemini, local models, and future agents are temporary workers. Project memory lives independently from them.

### Four thin layers

**Memory set** — declare only the documents that form the current project memory.  
**Project layout** — offer a native layout while allowing existing repositories to stay where they are.  
**Document annotation** — make Goal, State, Task, Decision, Evidence, Reference, and Artifact explicit.  
**AI language** — exchange typed, verifiable project state instead of repeating natural-language context.

```text
@task{id:#t42|goal:#g1|state:active|done:[#e69]|next:#a7}
@msg{op:resume|task:#t42|load:[#current,#e81]|skip:[#e69]|next:#a7}
```

A session may die. A browser may close. A machine may restart. A worker may be replaced. The TASK can continue from the same verified state.

### Deliberate non-goals

- no full conversation archive;
- no requirement to store prompts or responses;
- no vector database requirement;
- no model-vendor identity in the core protocol;
- no takeover of project truth;
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

Your project files remain the source of truth. Project memory stores only selection, type, references, state, and verification metadata.

---

## Quick start / 快速开始

```bash
python -m pip install -e .
resume-scene validate .
resume-scene checkpoint .
resume-scene resume .
```

Expected machine output / 预期机器输出：

```text
@checkpoint{id:#c_...|project:#resume_scene|task:#t0|memory:#m0|fingerprint:sha256:...}
@msg{op:resume|task:#t0|load:[#project,#current,#protocol,...]|skip:[]|next:#a0}
```

The repository dogfoods its own format: its current project state is already represented by `PROJECT.rsm`, `CURRENT.rsm`, and `.resume/memory.rsm`.

仓库本身已经用同一套格式记录自己的项目现场：`PROJECT.rsm`、`CURRENT.rsm` 与 `.resume/memory.rsm`。

License / 许可证：MIT.

## v0.1

`v0.1` is intentionally small: deterministic frames, validation, project-memory selection, checkpoint fingerprints, and resumable TASK state.
