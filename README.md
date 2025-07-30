# agent

> A **self‑modifying, Pydantic‑AI‑powered code‑writing assistant**  
> *(work in progress – breaking changes likely!)*

---

## ✨ Key capabilities

| Capability | What it means |
| -----------| ------------- |
| **Self‑modification** | `agent.core.self_modify()` can rewrite its own source tree safely & atomically (automatic `.bak` backups, no half‑written files). |
| **Pydantic‑AI integration** | Uses the [`pydantic‑ai`](https://pydantic-ai.readthedocs.io) ecosystem to generate, validate, and execute AI‑authored patches. |
| **CLI stub** | A tiny `agent` console command (`agent --help`) ready to grow into a REPL or service. |
| **First‑class dev‑container** | Dockerfile + `docker-compose.yaml` + `./dev.sh` script for an *instant* and reproducible sandbox. |
| **Safe dual‑version workflow** | Inside the container you always have two copies of *agent*: `stable` (pip‑installed, known‑good) and `working` (the live, editable checkout). Promote when ready—no rebuild needed. |

---

## 1️⃣  Using *agent* **as a normal library**

### Installation

```bash
pip install "agent @ git+https://github.com/Tuee22/agent.git@main"
```

or add to pyproject.toml
```toml
agent = { git = "https://github.com/Tuee22/agent.git", rev = "main" }
```