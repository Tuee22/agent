# Agent – A Self‑Modifying, Pydantic‑AI‑Driven Code Assistant

> **Status:** Proof‑of‑concept skeleton | **Type safety:** `mypy --strict` clean | **License:** MIT  

**Agent** is a pure‑Python **library + CLI** that embeds a large Python code‑base into an in‑process vector store and drives an ✨ *intelligent refactoring loop* ✨ powered by [Pydantic AI](https://docs.pydantic.dev/pydantic-ai/).  
It ships *batteries‑included*: deterministic offline embeddings, JSON‑persisted vector DB, and test / type‑check runners – all installable from GitHub with **no non‑Python services**.

---

## Table of Contents
1. [Features](#features)  
2. [Architecture](#architecture)  
3. [Installation](#installation)  
4. [Quick Start](#quick-start)  
   1. [CLI workflow](#cli-workflow)  
   2. [Python API](#python-api)  
5. [How It Works](#how-it-works)  
6. [Configuration](#configuration)  
7. [Extending](#extending)  
8. [Development](#development)  
9. [Docker](#docker)  
10. [FAQ](#faq)

---

## Features

| Capability                                   | Out‑of‑box? | Notes |
|----------------------------------------------|-------------|-------|
| Semantic code search (vector RAG)            | ✅          | In‑process JSON vector store (swap to Chroma later). |
| Offline deterministic embeddings             | ✅          | Hash‑based; swap‑in OpenAI easily. |
| CLI commands (`index`, `refactor`)           | ✅          | One‑liners for daily work. |
| Interactive agent via Python API             | ✅          | `agent.chat_sync(...)`. |
| Test‑driven validation (`pytest`)            | ✅          | Returns pass/fail + logs. |
| Static typing enforcement (`mypy`)           | ✅          | `--strict` passes itself. |
| File read/write tools with auto‑re‑indexing  | ✅          | No stale vectors. |
| Polling file‑watcher for external edits      | ✅          | Optional; pure‑Python. |
| MCP clients (Git, Filesystem, Run‑Python)    | 🅾 stub     | Interfaces defined; plug servers later. |
| Real LLM & embeddings (OpenAI)               | 🅾 stub     | Provide API key & swap embedder. |

---

## Architecture

```
src/agent
│
├─ config.py        ← Central typed settings
├─ main.py          ← Agent factory & tool registry
│
├─ embeddings/      ← Chunker, hash‑embeddings, JSON vector DB
├─ tools/           ← LLM‑callable helpers (search, tests, mypy, exec, IO)
├─ watcher/         ← Optional polling FS watcher
│
├─ cli/             ← Typer CLI  (entry‑point: `agent`)
└─ gui/             ← Minimal FastAPI stub (future AG‑UI)
```

Every module is implemented and passes `mypy --strict`; only the optional MCP
clients remain `NotImplementedError`.

---

## Installation

### Quick install (pip + GitHub)

```bash
pip install "git+https://github.com/Tuee22/agent.git#egg=agent"
```

### Editable clone (recommended for hacking)

```bash
git clone https://github.com/Tuee22/agent.git
cd agent
pip install -e ".[dev]"          # or: poetry install --with dev
```

Optional sanity check:

```bash
pytest -q                  # unit tests
mypy --strict src tests    # type safety
```

---

## Quick Start

Assume your project lives in `~/projects/acme/`.

### CLI workflow

```bash
cd ~/projects/acme               # target repo

# 1️⃣ build/refresh local vector index (one‑time)
agent index

# 2️⃣ refactor a module to async I/O
agent refactor --module src/data_processing.py                --objective "convert blocking I/O to asyncio and clarify naming"
```

What happens:

1. Agent retrieves semantic context for the file.  
2. LLM proposes an async refactor patch.  
3. File is written **and re‑indexed**.  
4. `pytest` and `mypy --strict` run; results printed.

### Python API

```python
from agent import get_agent

agent = get_agent()

prompt = """ 
Refactor 'src/data_processing.py':
• Replace synchronous HTTP with aiohttp
• Ensure unit tests and static types pass
"""
reply = agent.chat_sync(prompt)
print(reply.message.content)

# Examine individual tool calls
for call in reply.tool_calls:
    print(call.tool_name, "=>", call.output_summary)
```

---

## How It Works

1. **Embedding index**  
   * Files → 400‑line chunks → 128‑D hash embeddings.  
   * Stored with line‑range metadata in `.agent/chroma/vectors.jsonl`.  
2. **Tools**  
   * `read_file` / `write_file` (write triggers re‑embedding).  
   * `code_search` performs cosine search for RAG context.  
   * `run_tests` executes `pytest`; `run_mypy` enforces `mypy --strict`.  
3. **Agent loop**  
   * Pydantic AI’s LLM decides which tool to call next; results feed back.  
4. **Consistency**  
   * Polling watcher (optional) re‑embeds files touched outside the agent.

---

## Configuration

Environment variables (`AGENT_*`) override defaults:

| Variable                  | Default               | Purpose |
|---------------------------|-----------------------|---------|
| `AGENT_PROJECT_ROOT`      | `.`                   | Repo root to index. |
| `AGENT_CHROMA_DIR`        | `.agent/chroma`       | Persistence folder. |
| `AGENT_MODEL_NAME`        | `gpt-4o-mini`         | LLM choice. |
| `AGENT_EMBEDDINGS_MODEL`  | `gpt-embeddings-mini` | (if using OpenAI). |
| `AGENT_OPENAI_API_KEY`    | _empty_               | Enable real embeddings/LLM. |

Switch to OpenAI embeddings:

```python
from openai import OpenAI
from agent.embeddings.indexer import EmbeddingClient

class OpenAIClient(EmbeddingClient):
    def __init__(self, key: str) -> None:
        self._client = OpenAI(api_key=key)

    def embed(self, text: str) -> list[float]:
        rsp = self._client.embeddings.create(
            input=text, model="text-embedding-3-small"
        )
        return rsp.data[0].embedding
```

Pass an `OpenAIClient` wherever `HashEmbeddingClient` is used.

---

## Extending

* **Vector DB** – implement `VectorStore` using Chroma/FAISS.  
* **MCP servers** – finish stubs in `agent/mcp/` to integrate Git, FS, etc.  
* **New tools** – add typed function in `agent/tools/`, register it in `agent/main.py`.  
* **GUI** – expand `agent/gui/app.py` with a Pydantic AI AG‑UI or Streamlit.

---

## Development

```bash
poetry install --with dev
pytest -q
mypy --strict src tests
black --check src tests
```

### Contribution Guidelines

* No `Any` or `# type: ignore` in committed code.  
* Public functions/classes are documented.  
* Aim for > 90 % test coverage.

---

## Docker

```bash
docker compose -f docker/docker-compose.yaml up --build
```

Starts **JupyterLab** at <http://localhost:9999>; host repo is mounted at `/workspace`.

---

## FAQ

<details>
<summary><strong>Does it really modify my files?</strong></summary>

Yes. The agent writes directly to your working tree after the LLM chooses a diff
and validations pass. Always commit or back up first—or run it on a branch.
</details>

<details>
<summary><strong>How large a code‑base can it handle?</strong></summary>

The bundled JSON vector store scales comfortably to ~100 k LOC.  
For monorepos swap to Chroma or another ANN engine.
</details>

<details>
<summary><strong>Why use hash‑based embeddings by default?</strong></summary>

It keeps the project 100 % offline, free, and deterministic. Real embeddings are one `EmbeddingClient` away.
</details>

<details>
<summary><strong>Is the agent asynchronous?</strong></summary>

Current tools are synchronous; Pydantic AI supports async if you need it.
</details>

---

*Happy hacking — and remember: type‑safety first, hallucinations second 😉*
