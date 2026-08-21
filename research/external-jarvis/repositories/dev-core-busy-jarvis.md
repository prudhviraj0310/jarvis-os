# Research Inspection: dev-core-busy / jarvis

- **Repository URL**: `https://github.com/dev-core-busy/jarvis`
- **Primary License**: Apache License 2.0
- **Primary Languages**: Python 3.11+, TypeScript/Vue.js (Frontend), Go (Windows app)
- **Primary Frameworks**: FastAPI, Celery/Redis, Docker/Seccomp, PyAutoGUI, Playwright, LiteLLM

---

## 1. System Architecture
`dev-core-busy/jarvis` uses an enterprise-grade client-server microservice model:
* **Backend (`backend/`)**: FastAPI central daemon hosting the agent runtime, task graph, and LLM routers.
* **Agent Engine (`backend/agent.py`)**: 250KB monolithic hierarchical planner with dynamic sub-agents (`coding_agent`, `vision`, `support_assistant`).
* **Execution Sandbox (`backend/sandbox.py`, `backend/sandbox_guard.py`)**: Confinement using Docker containers and Linux seccomp profiles for untrusted tool execution.
* **Desktop Control (`backend/desktop_control.py`, `skills/desktop/`)**: PyAutoGUI/Xdotool mouse/keyboard control with VNC/noVNC web observation.
* **Skills System (`skills/`)**: 33 modular skills (WhatsApp, Email, Telegram, Browser, Confluence, SAP, JIRA, Vision).

---

## 2. Major Capabilities
1. **Multi-Channel Hub**: WhatsApp, Telegram, Email, Slack, Microsoft Office Add-in.
2. **Autonomous Task Execution**: Multi-step plan generation with replanning on tool failures.
3. **Continuous Knowledge & RAG (`backend/knowledge_sync.py`, `backend/learning.py`)**: Periodic vector store compaction and automated learning from past interactions.
4. **Sandboxed Execution**: Isolated execution of generated Python/Bash scripts inside ephemeral Docker containers.
5. **Model Routing (`backend/llm.py`, `backend/model_caps.py`)**: Auto-routes between Claude 3.5 Sonnet, GPT-4o, and local Ollama based on cost, speed, and context size.

---

## 3. Entry Points & Key Modules
* **CLI / Service Entry**: `backend/main.py`, `run_jarvis.py`, `jarvis.service` (systemd unit).
* **Agent Core**: `backend/agent.py` (`AgentRunner`, `execute_step()`, `evaluate_goal()`).
* **Email Runner**: `backend/mail_runner.py` (Background IMAP poller and automated classification).
* **Desktop Automator**: `backend/desktop_control.py` (Coordinate mapping, active window tracking).
* **Tool Host**: `backend/mcp_client.py` (Model Context Protocol client).

---

## 4. Dependencies
* `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `redis`, `celery`
* `playwright`, `pyautogui`, `pytesseract`, `opencv-python`
* `litellm`, `langchain-core`, `chromadb`, `sentence-transformers`

---

## 5. Security & Machine Sovereignty Analysis
* **Egress Guard (`backend/egress_guard.py`)**: Inspects outbound network payloads for API key leaks.
* **Sandbox Guard (`backend/sandbox_guard.py`)**: Checks shell commands against a whitelist of dangerous patterns (`rm -rf`, `mkfs`, fork bombs).
* **Limitation**: The agent can run autonomous destructive commands if configured in "full autonomy" mode without human confirmation gates.

---

## 6. What Can Be Adapted to JARVIS OS
* **Modular Skills Directory Structure**: Clean skill definition with YAML metadata and isolated dependencies.
* **Continuous Learning Pipeline (`learning.py`)**: Storing success/failure reflections into a persistent local knowledge base.
* **Multi-LLM Capability Routing Matrix**: Deciding whether a task requires fast edge inference or deep multi-agent reasoning.

---

## 7. What is NOT Suitable
* Heavy Python Web Stack (Celery, Redis, SQLAlchemy) — In JARVIS OS, this must run as a native C++/Rust microservice daemon or lightweight local process.
* Direct unconfirmed execution loops — JARVIS OS requires the `PolicyGate` confirmation invariant.

---

## 8. License Compliance
* **Apache 2.0**: Fully permissive for commercial use and modification. Attribution in `NOTICE` file required if code is directly adapted.
