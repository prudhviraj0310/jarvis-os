# Research Inspection: LakshyaBadjatya / Friday

- **Repository URL**: `https://github.com/LakshyaBadjatya/Friday`
- **Primary License**: MIT License
- **Primary Languages**: Python 3.11+, TypeScript, Svelte / React, HTML5/CSS3
- **Primary Frameworks**: FastAPI, LiteLLM, Playwright, SQLite/PostgreSQL, Firebase/Firestore, PWA

---

## 1. System Architecture
`LakshyaBadjatya/Friday` is an ambitious personal AI operating system architecture structured around deterministic pipelines and fail-closed security:
* **Deterministic Orchestrator (`src/friday/agent/`)**: Strict separation between the planner, coordinator, and domain specialist sub-agents (`email`, `calendar`, `browser`, `vault`, `circle`, `market`).
* **Execution Flow & Replanning (`src/friday/flows/`)**: Explicit flow state machine with simulation before execution (`simulate.py`, `replan.py`).
* **Security & Action Broker (`src/friday/security/`)**: Fail-closed permission system; sensitive actions generate human approval tickets.
* **Personal Vault & Knowledge Graph (`src/friday/vault/`)**: Notes, exam materials, structured documents, and semantic embeddings with Firestore syncing.
* **Perception Engine (`src/friday/perception/`)**: Screen watcher, clipboard monitor, and OCR text extractor.

---

## 2. Major Capabilities
1. **Flow Simulation & Replanning**: Before executing complex workflows, Friday simulates potential failure modes and asks for confirmation.
2. **Personal Circle & Social Intelligence (`src/friday/circle/`)**: Models contacts, relationships, past promises, and care check-ins.
3. **Multi-Interface Hub**: PWA mobile interface, desktop HUD, TUI (Terminal UI), and Android/TV companion apps.
4. **Market & Finance Integration (`src/friday/market/`)**: Live financial market streaming and order execution guardrails.

---

## 3. Entry Points & Key Modules
* **Core Agent**: `src/friday/agent/friday.py`, `src/friday/agent/orchestrator.py`.
* **Flow Engine**: `src/friday/flows/engine.py`, `simulate.py`.
* **Action Security Broker**: `src/friday/security/action_broker.py`.
* **HUD Server**: `src/friday/hud/`.

---

## 4. Dependencies
* `fastapi`, `pydantic`, `litellm`, `playwright`, `sqlite3`, `firebase-admin`, `tesseract`

---

## 5. Security & Machine Sovereignty Analysis
* **Exceptional Alignment with JARVIS OS**: Friday implements strict fail-closed action brokering where no irreversible action (sending money, emailing, deleting files) can execute without an explicit cryptographic signature or user prompt.

---

## 6. What Can Be Adapted to JARVIS OS
* **Flow Simulation & Replanning Pattern**: Asking "Simulate action consequences before execution."
* **Personal Circle & Relationship Graph**: Storing promises, commitments, and contact importance scores.
* **Action Security Broker Architecture**: Standardized token-based confirmation ticket flow.

---

## 7. What is NOT Suitable
* Cloud Firebase/Firestore lock-in — Must be strictly local in JARVIS OS (`/etc/jarvis/vault/`).

---

## 8. License Compliance
* **MIT License**: Fully permissive for commercial use and modification with copyright attribution.
